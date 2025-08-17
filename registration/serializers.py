from rest_framework import serializers
from django.contrib.auth.models import Group
from registration.models import Customer
from phonenumber_field.serializerfields import PhoneNumberField
import re
class CustomerSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(region="KE")
    
    username = serializers.CharField(
        max_length=150,
        validators=[]  # remove default email validator
    )
    
    class Meta:
        model = Customer
        fields = ("username", "phone_number")
        
    

    def validate_username(self, value):
        # Allow both normal strings and emails
        email_pattern = r"[^@]+@[^@]+\.[^@]+"
        if re.match(email_pattern, value):
            return value  # valid email
        if value.isalnum():  # or apply your own rules for usernames
            return value
        raise serializers.ValidationError("Username must be a valid email or alphanumeric string.")