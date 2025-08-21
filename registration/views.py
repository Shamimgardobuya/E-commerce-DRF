from registration.models import Customer
from registration.serializers import CustomerSerializer, Auth0UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from registration.utils import Auth0JWTAuthentication, assign_role, RequiresScope, get_username_from_payload
from django.conf import settings
import requests
from django.http import JsonResponse
import http.client
import urllib.parse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 
from django.conf import settings
from rest_framework import status
from e_commerce.auth0_token import get_management_token
import jwt
@swagger_auto_schema(
    request_body=Auth0UserSerializer,
    method='post',
    operation_description="Registering as an auth user",
    responses={201: "User created successfully", 500: "Error occurred"}
    
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_auth_user(request):
    token = get_management_token()

    serializer = Auth0UserSerializer(data= request.data)
    serializer.is_valid(raise_exception=True)
    data_validated = serializer.validated_data
    
    payload = data_validated

    user_url = f"https://{settings.AUTH0_DOMAIN}/api/v2/users"

    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
        }

    try:
        response = requests.post(user_url, json=payload, headers=header)
        return Response({
            "message": "User created successfully",
            "data": response.json()
        },status=status.HTTP_201_CREATED)
    except Exception:
        return Response({
            "message": "Error occurred",
            "data": []
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="post",
    request_body=CustomerSerializer,
    operation_description="Performs authentication by auth0 and creates customer",
    responses={201: "User authenticated successfully", 400: "Bad request"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def request_token(request):
    try:
        serializer = CustomerSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        data_validated = serializer.validated_data


        token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
        payload = {
            "grant_type": "password",
            "username": data_validated.get('username'),
            "password": data_validated.get('password'),
            "audience": settings.AUTH0_AUDIENCE,
            "scope": "openid profile email read:categories create:categories create:orders create:products delete:categories delete:orders delete:products read:categories read:orders read:products update:categories update:orders update:products",
            "client_id": settings.AUTH0_WEB_CLIENT_ID,
            "client_secret": settings.AUTH0_WEB_CLIENT_SECRET
        }

        role_to_assign = settings.AUTH0_ADMIN_ROLE if data_validated.get('role') == "Admin" else settings.AUTH0_CUSTOMER_ROLE
        response = requests.post(token_url, json=payload)

        resp_data = response.json()
        if response.status_code == 200:
            access_token = resp_data.get("access_token")
            decoded_token = Auth0JWTAuthentication.decode_token(access_token)
            open_id = decoded_token.get('sub')
            username = get_username_from_payload(open_id)
            assign_role(open_id, role_to_assign)
            customer, created = Customer.objects.get_or_create(open_id=open_id
                        )
            if customer:
                customer.phone_number = data_validated.get("phone_number")
                customer.username = username
                customer.role = data_validated.get('role') if data_validated.get('role') else "Customer"
                customer.save()
            return Response({
                "message": "Authenticated successfully.",
                "access_token": access_token,
                "token_type": "Bearer",
                "expires_in": decoded_token.get('exp')

            }, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {"error": "network_error", "details": str(e)},
            status=503,
        )
    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {"error": "network_error", "details": str(e)},
            status=503,
        )
        
    except jwt.exceptions.ExpiredSignatureError as e:
        return JsonResponse(
            {"error": "Signature has expired", "details": str(e)},
            status=500,
        )
        