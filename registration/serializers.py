from rest_framework import serializers
from django.contrib.auth.models import Group
from registration.models import Customer
from phonenumber_field.serializerfields import PhoneNumberField
import re



class Auth0UserSerializer(serializers.Serializer):
    """
    Serializer for creating a new user in Auth0.
    """
    connection = serializers.CharField(
        
        default="Username-Password-Authentication",
        help_text="The name of the Auth0 connection (e.g., 'Username-Password-Authentication').",
        
    )
    email = serializers.EmailField(
        required=True,
        help_text="The user's email address."
    )
    password = serializers.CharField(
        write_only=True,
        max_length=128,
        help_text="The user's password. This field is write-only for security."
    )

    user_id = serializers.CharField(
        required=False,
        max_length=255,
        help_text="A custom user ID. Auth0 will generate one if not provided."
    )
    given_name = serializers.CharField(
        required=False,
        max_length=100,
        help_text="The user's first name."
    )
    family_name = serializers.CharField(
        required=False,
        max_length=100,
        help_text="The user's last name."
    )
    name = serializers.CharField(
        required=False,
        max_length=200,
        help_text="The user's full name."
    )
    picture = serializers.URLField(
        required=False,
        help_text="A URL to your user's profile picture."
    )
    blocked = serializers.BooleanField(
        required=False,
        help_text="Indicates if  user is blocked."
    )
    verify_email = serializers.BooleanField(
        required=False,
        help_text="Whether to send a verification email to the user."
    )
    user_metadata = serializers.JSONField(
        required=False,
        help_text="Metadata that can be read by the client application."
    )
    app_metadata = serializers.JSONField(
        required=False,
        help_text="Metadata that can only be read by the Management API."
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
    
