from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from registration.models import Customer

# class CustomerApiTest(APITestCase):
#     def setUp(self):
#         self.customer = Customer.objects.create(username="serin@gmail", phone_number="111222333")
#         self.url = reverse("register") 
        
#     def test_create_customer(self):
#         new_customer = Customer.objects.create(open_id="newuse78989889r", username = "username@gmail.com",phone_number="03438473847")
#         data = {"username": "shakora@gmail.com", "phone_number": "444555666", "password": "N323$ir''^%A", "role":"Admin"}
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # self.assertEqual(Customer.objects.count(), 2)

#     def test_retrieve_customer(self):
#         detail_url = reverse("customer-detail", args=[self.customer.open_id])
#         response = self.client.get(detail_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["phone_number"], "111222333")
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings
from registration.models import Customer


class RequestTokenTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("request_token")  # match your urlpattern name
        self.payload = {
            "role": "Admin",
            "username": "testuser@gmail.com",
            "password": "password123",
            "phone_number": "075 534 4783"
        }

    @patch("registration.views.requests.post")  # mock requests.post
    @patch("registration.utils.Auth0JWTAuthentication.decode_token")  # mock decoder
    @patch("registration.utils.assign_role")  # mock role assigner
    def test_request_token_success(
        self, mock_assign_role, mock_decode_token, mock_post
    ):
        print("mock_post called?", mock_post.called)

        # Mock Auth0 token response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "fake_access_token"
        }
        mock_post.return_value = mock_response

        # Mock decode_token to return payload
        mock_decode_token.return_value = {
            "sub": "auth0|12345",
            "exp": 9999999999
        }

        # Perform request
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

        # Check customer was created
        self.assertTrue(Customer.objects.filter(open_id="auth0|12345").exists())
        customer = Customer.objects.get(open_id="auth0|12345")
        self.assertEqual(customer.phone_number, "123456789")
        self.assertEqual(customer.username, "testuser")

        # Check mocks called
        mock_assign_role.assert_called_once_with("auth0|12345","Admin")

    @patch("registration.views.requests.post")
    def test_request_token_failure_from_auth0(self, mock_post):
        # Mock Auth0 error response
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": "invalid_grant"}
        mock_post.return_value = mock_response

        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    @patch("registration.views.requests.post")
    def test_request_token_exception(self, mock_post):
        # Simulate exception
        mock_post.side_effect = Exception("Network error")

        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn("error", response.data)
