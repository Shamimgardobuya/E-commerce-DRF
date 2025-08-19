from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Product
from categories.models import Category
from unittest.mock import patch
from registration.models import Customer

@patch('registration.utils.Auth0JWTAuthentication.decode_token')
@patch('registration.utils.Auth0JWTAuthentication.authenticate')
class ProductApiTest(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.get_or_create(open_id='test-user-id')
        self.category = Category.objects.create(category_name="Appliances")
        self.child_category = Category.objects.create(category_name="House Appliances",parent=self.category)
        self.product = Product.objects.create(name="Fridge", price=200.00, category=self.category,weight=34,quantity=45, units="grams")
        
    def test_list_products(self, mock_authenticate, mock_decode_token):
        url = reverse("product-list")
        mock_authenticate.return_value = (Customer.objects.get(open_id='test-user-id'), 'fake-token')
        mock_decode_token.return_value = {
            'sub': 'test-user-id',
            'scope': 'read:products'
        }
        headers = {'HTTP_AUTHORIZATION': 'Bearer fake-token'}

        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self, mock_authenticate, mock_decode_token):
        mock_authenticate.return_value = (Customer.objects.get(open_id='test-user-id'), 'fake-token')
        mock_decode_token.return_value = {
            'sub': 'test-user-id',
            'scope': 'create:products read:products'
        }
        headers = { 'HTTP_AUTHORIZATION' : 'Bearer fake-token'}
        data = {"name": "Microwave", "price": 100.00, "category": {"Appliances": "House Appliances"}, "quantity": 10, "weight": 5, "units": "grams"}
        url = reverse("product-list")
        response = self.client.post(url, data, **headers, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_product(self, mock_authenticate, mock_decode_token):
        mock_authenticate.return_value = (Customer.objects.get(open_id='test-user-id'), 'fake-token')
        mock_decode_token.return_value = {
            'sub': 'test-user-id',
            'scope': 'create:products read:products'
        }
        detail_url = reverse("product-detail", args=[self.product.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["name"], "Fridge")
