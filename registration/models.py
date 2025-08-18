from django.db import models
from django.contrib.auth.models import  AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, timedelta
from django.utils import timezone
# Create your models here.


class Customer(models.Model):
    open_id = models.CharField(max_length=255, unique=True)
    username = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, default="Customer")

    class Meta:
        verbose_name_plural = "Customers"
  
    
    @property
    def is_authenticated(self):
        return True  # every Customer from Auth0 is considered authenticated