from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from orders.models import Order
from registration.models import Customer
from categories.models import Category
from products.models import Product

class OrderApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="orderapi", password="pass123")
        self.customer = Customer.objects.create(username=self.user.username, phone_number="999888777", open_id="aut3434938434")
        self.order = Order.objects.create(customer=self.customer)
        category = Category.objects.create(category_name="Gadgets")
        product = Product.objects.create(name="Smartphone", price=500.00, category=category, quantity=34, weight=50)
        self.url = reverse("orders")

    def test_list_orders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        #create product and category instance
        data = {"customer": self.customer.id, "products": [ { "product": self.product.id, "quantity": 2}]}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_order(self):
        detail_url = reverse("order-detail", args=[self.order.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "pending")
