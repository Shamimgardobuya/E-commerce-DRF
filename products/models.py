from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from categories.models import Category
# Create your models here.
    
class Product(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey(Category,null=False, on_delete=models.PROTECT )
    quantity = models.IntegerField(null=False)
    units = models.CharField(max_length=27, null=False, default='grams')
    weight = models.IntegerField(null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, default=0.00, decimal_places=2)
    
    class Meta:
        verbose_name_plural = "Products"
    
    def __str__(self):
        return f"product name : {self.name}, quantity {self.quantity}, weight {self.weight}, price{self.price} "
    