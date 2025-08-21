import requests
from django.conf import settings
from django.core.cache import cache
import time
_CACHE_KEY = "auth0:mgmt:token"
_SAFETY_BUFFER = 60


def _fetch_new_token():
    resp = requests.post(
        f"https://{settings.AUTH0_DOMAIN}/oauth/token",
        json={
                'grant_type': 'client_credentials',
                'client_id': settings.AUTH0_MGMT_CLIENT_ID,
                'client_secret': settings.AUTH0_MGMT_CLIENT_SECRET,
                'audience': f"https://{settings.AUTH0_DOMAIN}/api/v2/"
            
        }
        ,
        timeout=10
    )
    resp.raise_for_status()
    data = resp.json()
    expires_at = time.time() + int(data['expires_in']) - _SAFETY_BUFFER
    
    token_data = {
        "access_token": data["access_token"],
        "expires_at": expires_at
    }
    ttl = max(1, int(expires_at-time.time()))
    cache.set(_CACHE_KEY, token_data, ttl)
    return token_data

def get_management_token():
    token_data = cache.get(_CACHE_KEY)
    if token_data and token_data.get("expires_at", 0) > time.time():
        return token_data["access_token"]
    token_data = _fetch_new_token()
    return token_data["access_token"]
        