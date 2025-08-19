from rest_framework import serializers
from django.contrib.auth.models import Group
from registration.models import Customer
from phonenumber_field.serializerfields import PhoneNumberField
import re



class Auth0UserSerializer(serializers.Serializer):
    """
    Serializer for creating a new user in Auth0.
    """
    connection = serializers.HiddenField(
                default="Username-Password-Authentication"
        
    )
    email = serializers.EmailField(
        required=True,
        help_text="user's email address."
    )
    password = serializers.CharField(
        write_only=True,
        max_length=128,
        help_text="user's password"
    )


    def validate(self, data):
        if 'email' not in data:
            raise serializers.ValidationError("An 'email' field is required.")
        if 'password' not in data:
            raise serializers.ValidationError("A 'password' field is required.")
        
        return data
class CustomerSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(region="KE")
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(
        write_only=True, required=False,
        help_text="The role of the user can either be Admin or Customer. If left blank, default role will be customer."
    )


    class Meta:
        model = Customer
        fields = ("username", "phone_number", "password", "role")
        

    def validate_username(self, value):
        email_pattern = r"[^@]+@[^@]+\.[^@]+"
        if re.match(email_pattern, value):
            return value  
        if value.isalnum():  
            return value
        raise serializers.ValidationError("Username must be a valid email or alphanumeric string.")
    
