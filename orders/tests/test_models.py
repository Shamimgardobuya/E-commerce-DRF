from django.test import TestCase
from orders.models import Order
from products.models import Product, Category
from orders.models import OrderProduct
from registration.models import Customer
from django.contrib.auth.models import User
from django.core.cache import cache

class OrderProductModelTest(TestCase):
    def setUp(self):
        # user = User.objects.create_user(username="pivotuser", password="pass123")
        customer = Customer.objects.create(username="testing ", phone_number="222333444", open_id="897tyt")
        order = Order.objects.create(customer=customer)
        category = Category.objects.create(category_name="Gadgets")
        product = Product.objects.create(name="Smartphone", price=500.00, category=category)
        self.order_product = OrderProduct.objects.create(order=order, product=product, quantity=2)

    def test_order_product_quantity(self):
        self.assertEqual(self.order_product.quantity, 2)

    def test_order_product_relation(self):
        self.assertEqual(self.order_product.order.customer.user.username, "testing")
        self.assertEqual(self.order_product.product.name, "Smartphone")
    
    def tearDown(self):
        cache.clear()
        super().tearDown()