from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=25, null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,related_name="subcategories")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True,blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.category_name} > {self.category_name}"
        return self.category_name
    