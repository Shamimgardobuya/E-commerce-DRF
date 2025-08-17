from rest_framework import serializers
from orders.models import Order, OrderProduct
from registration.models import Customer
from products.models import Product

class OrderProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'products']
        read_only_fields = ['customer']  

#check product id to exist before creating an order 
    def create(self, validated_data):
        request = self.context.get("request")

        items_data = validated_data.pop("products")
        customer = request.user  
        
        
        order = Order.objects.create(customer=customer, **validated_data)

        for item in items_data:
            OrderProduct.objects.create(order=order, **item)

        return order
    
    
    def update(self, instance, validated_data):
        items_data = validated_data.pop('products', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if items_data:
            for item in items_data:
                order_product_instance = OrderProduct.objects.get(order=instance, product = item.get('product'))
                order_product_instance.quantity = item.get('quantity')
                order_product_instance.save()
        return instance
