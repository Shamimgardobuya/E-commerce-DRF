from django.db import models
from registration.models import Customer
from products.models import Product
from django.utils import timezone

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True,related_name="customer")
    products = models.ManyToManyField(Product, through='OrderProduct', null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    @property
    def total_price(self):
        return sum(
            item.quantity * item.product.price
            for item in self.order_products.all()
        )
    


    class Meta:
        verbose_name_plural = "Orders"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
   
    
    
