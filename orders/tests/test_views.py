from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from orders.models import Order
from products.models import Product
from categories.models import Category
from registration.models import Customer

@patch('registration.utils.Auth0JWTAuthentication.decode_token')
@patch('registration.utils.Auth0JWTAuthentication.authenticate')
class OrderApiTest(APITestCase):
    def setUp(self):
        self.customer, _ = Customer.objects.get_or_create(open_id='test-user-id')
        self.category = Category.objects.create(category_name="Gadgets")
        self.product = Product.objects.create(name="Smartphone", price=500.00, category=self.category, quantity=34, weight=50)
        self.order = Order.objects.create(customer=self.customer)
        self.url = reverse("orders-list")

    def mock_auth(self, mock_authenticate, mock_decode_token, scope):
        mock_authenticate.return_value = (self.customer, 'fake-token')
        mock_decode_token.return_value = {
            'sub': self.customer.open_id,
            'permissions': scope
        }
        return {'HTTP_AUTHORIZATION': 'Bearer fake-token'}

    def test_list_orders(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token, ['read:orders'])
        response = self.client.get(self.url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token, ['create:orders', 'read:orders'])
        data = {"products": [ { "product": self.product.id, "quantity": 2}]}
        response = self.client.post(self.url, data, **headers, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_order(self, mock_authenticate, mock_decode_token):
        detail_url = reverse("order-detail", args=[self.order.id])
        headers = self.mock_auth(mock_authenticate, mock_decode_token,['read:orders'])
        response = self.client.get(detail_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
