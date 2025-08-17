from registration.models import Customer
from registration.serializers import CustomerSerializer
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


@api_view(['POST'])
@permission_classes([AllowAny])
def request_token(request):
    try:

        role = request.data.get('role')
        username = request.data.get('username')
        password = request.data.get("password")
        phone_number = request.data.get("phone_number")
        serializer = CustomerSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)


        token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
        payload = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "audience": settings.AUTH0_AUDIENCE,
            "scope": "openid profile email read:categories create:categories create:orders create:products delete:categories delete:orders delete:products read:categories read:orders read:products update:categories update:orders update:products",
            "client_id": settings.AUTH0_WEB_CLIENT_ID,
            "client_secret": settings.AUTH0_WEB_CLIENT_SECRET
        }

        role_to_assign = settings.AUTH0_ADMIN_ROLE if role == "admin" else settings.AUTH0_CUSTOMER_ROLE
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
                customer.phone_number = phone_number
                customer.username = username 
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
@api_view(['GET'])
@permission_classes([AllowAny])
def get_management_token(request):
    try:
        conn = http.client.HTTPSConnection(settings.AUTH0_DOMAIN)

        payload = urllib.parse.urlencode({
                'grant_type': 'client_credentials',
                'client_id': settings.AUTH0_MGMT_CLIENT_ID,
                'client_secret': settings.AUTH0_MGMT_CLIENT_SECRET,
                'audience': f"https://{settings.AUTH0_DOMAIN}/api/v2/"
            })

        headers = { 'content-type': "application/x-www-form-urlencoded" }

        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        data = res.read()
        
        return Response({"message": "Token feteched successfuly", "access_token": data.decode("utf-8")})
    except Exception as e:
        return Response({"message": f"Error occurred ... {str(e)}"})
    
    
