from django.contrib import admin
from registration.models import Customer
from products.models import Product
from categories.models import Category
from orders.models import Order,  OrderProduct

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)
class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)

class OrdersAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrdersAdmin)

class OrdersProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrderProduct, OrdersProductAdmin)

