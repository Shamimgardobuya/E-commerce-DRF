from django.conf import settings
import json
from authlib.integrations.django_client import OAuth
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
import requests

class Sms:
    def __init__(self, client_id):
        pass
    
    def send_sms(message):
        return message