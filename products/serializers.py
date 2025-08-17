
from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id","category","name","quantity", "weight", "units")
        
        
        def value_units(self, value):
            units_ =  ['grams','kilograms','milliliters', 'liters']
            if value not in units_:
                raise serializers.ValidationError(f"Units of product needs to be either one of these {units_}")
            return value