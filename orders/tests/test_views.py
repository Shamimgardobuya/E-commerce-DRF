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
        self.product_a, create_new_product = Product.objects.get_or_create(name="Smartphone", price=500.00, category=self.category, quantity=34, weight=50)
        self.product_b, create_product = Product.objects.get_or_create(name="Tablet", price=6500.00, category=self.category, quantity=67, weight=50)
        self.order, new_order = Order.objects.get_or_create(customer=self.customer)
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
        data = {"products": [ { "product": self.product_a.id, "quantity": 2}]}
        response = self.client.post(self.url, data, **headers, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_order(self, mock_authenticate, mock_decode_token):
        detail_url = reverse("order-detail", args=[self.order.id])
        headers = self.mock_auth(mock_authenticate, mock_decode_token,['read:orders'])
        response = self.client.get(detail_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_order(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token, ['create:orders', 'read:orders'])
        data = {"products": [ { "product": self.product_b.id, "quantity": 5}]}
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.put(url, data, **headers, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order(self, mock_authenticate, mock_decode_token):
        headers = self.mock_auth(mock_authenticate, mock_decode_token, ['delete:orders'])
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.delete(url, **headers, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        return super().tearDown()