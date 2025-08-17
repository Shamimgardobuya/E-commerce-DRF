from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Product
from categories.models import Category

class ProductApiTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name="Appliances")
        self.product = Product.objects.create(name="Fridge", price=200.00, category=self.category,weight=34,quantity=45, units="grams")
        self.url = reverse("product-list")

    def test_list_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        data = {"name": "Microwave", "price": 100.00, "category": self.category.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_product(self):
        detail_url = reverse("product-detail", args=[self.product.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Fridge")
