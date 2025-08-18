from django.urls import path, include

from registration import views

from rest_framework import routers

urlpatterns = [
    path("login", views.request_token, name="request_token"),
    path("token", views.get_management_token, name="get_auth0_mgmt_token"),
    path("register", views.create_auth_user, name="create_user"),


]
