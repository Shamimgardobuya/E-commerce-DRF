from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from registration.models import Customer


# @receiver(post_save, sender=User)
# def create_customer_if_not_exist(sender, instance, created, **kwargs):
#     #when a user is created, confirm is there is a customer linked to the user
    
#     if created:
#         customer_exists = Customer.objects.filter(user=instance).exists()
        