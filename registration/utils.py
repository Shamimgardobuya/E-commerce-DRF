from rest_framework.authentication import BaseAuthentication
import requests
import json
import jwt
import os
from django.http import JsonResponse
from functools import wraps
from django.conf import settings
from dotenv import load_dotenv
import jwt
from django.db import connection
import http.client
from django.contrib.auth.models import User
from registration.models import Customer
from rest_framework import exceptions
from rest_framework import status

def assign_role(user_id, role_id):
    try:
        url = f"https://{settings.AUTH0_DOMAIN}/api/v2/users/{user_id}/roles"
        headers = { 'authorization': f"Bearer {settings.AUTH0_MGMT_API_TOKEN}" ,
                'Content-Type': "application/json"
                }
        payload = json.dumps({
        "roles": [
            role_id
        ]
        })
        roles = requests.get(url=url,headers=headers)
        if (roles):
            role_ids = [role['id'] for role in roles.json()]
            requests.delete(url=url, json={ "roles": role_ids }, headers=headers) #remove previous roles
        response = requests.post(url=url, data=payload, headers=headers)
        print(response.text)
    except Exception as e:
        raise e
        
    

cursor = connection.cursor()
class FindAverageProduct:
    def __init__(self,category_id):
        self.category_id = category_id
    
    def create_view(self):
    
        query = """
            WITH RECURSIVE subcategories AS (
                SELECT id
                FROM categories_category
                WHERE id = %s
                UNION ALL
                SELECT c.id
                FROM categories_category c
                INNER JOIN subcategories s ON c.parent_id = s.id
            )
            SELECT AVG(p.price) AS avg_price
            FROM products_product p
            WHERE p.category_id IN (SELECT id FROM subcategories)
        """
        cursor.execute(query, [self.category_id])

        row = cursor.fetchone()
        return row if row else None
        


class RequiresScope:
    def __init__(self, required_scope):
        self.required_scope = required_scope

    def __call__(self, func):
        @wraps(func)
        def wrapper(view_instance, request, *args, **kwargs):
            try:
                token = Auth0JWTAuthentication.get_token_from_header(request)
                decoded = Auth0JWTAuthentication.decode_token(token)
            except Exception as e:
                return JsonResponse({"message": f"Invalid token: {str(e)}"}, status=401)

            scopes = decoded.get("permissions", "")
            if self.required_scope not in scopes:
                return JsonResponse(
                    {"message": "You are not allowed to view this resource"}, status = status.HTTP_403_FORBIDDEN
                )

            return func(view_instance, request, *args, **kwargs)

        return wrapper
    
    

class Auth0JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = self.get_token_from_header(request)
        
        if not token:# No token → allow permissions to decide
            return None
        try:
            payload = self.decode_token(token)

            if not payload:
                raise exceptions.AuthenticationFailed('Invalid token')
            print(">>"*10, payload.get('sub'))
            customer = Customer.objects.get(open_id=payload.get('sub'))

            return (customer,token)

        except Exception as e:
            raise e
        
    @staticmethod
    def get_token_from_header(request):
        header = request.headers.get("Authorization")
        
        if header:
            parts = header.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                raise exceptions.AuthenticationFailed("Authorization header must be Bearer token")
            return parts[1]

    

    @staticmethod
    def decode_token(token):
        header = jwt.get_unverified_header(token)

        if "kid" not in header:
            raise exceptions.AuthenticationFailed("Token header missing 'kid'")

        jwks_url = f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json'
        jwks = requests.get(jwks_url).json()

        public_key = None
        for jwk in jwks['keys']:
            if jwk['kid'] == header['kid']:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

        if public_key is None:
            raise exceptions.AuthenticationFailed("Public key not found")

        decoded = jwt.decode(
            token,
            public_key,
            audience=settings.AUTH0_AUDIENCE,
            issuer=f'https://{settings.AUTH0_DOMAIN}/',
            algorithms=['RS256']
        )
        return decoded


def get_username_from_payload(user_id):
        conn = http.client.HTTPSConnection(settings.AUTH0_DOMAIN)

        headers = {'authorization': f"Bearer {os.getenv('AUTH0_MGMT_API_TOKEN')}"}
        conn.request("GET", f"/api/v2/users/{user_id}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        dt = json.loads(data.decode("utf-8"))
            
        return dt.get("given_name") or dt.get("name")

