
from rest_framework import serializers
from products.models import Product
from categories.models import Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("category","name","quantity", "weight", "units", "price")

        
        def validate_units(self, value):
            units_ =  ['grams','kilograms','milliliters', 'liters']
            if value not in units_:
                raise serializers.ValidationError(f"Units of product needs to be either one of these {units_}")
            return value
        
        def create(self,validated_data):
            category = validated_data.pop("category")
            name = validated_data.pop("name"),
            quantity = validated_data.pop("quantity")
            weight = validated_data.pop("weight")
            price = validated_data.pop("price")
            for key, value in category.items():
                find_category = Category.objects.get(category_name=value)
                exist_product , create_product = Product.objects.get_or_create(
                    category = find_category,
                    name=name,
                    quantity=quantity,
                    weight=weight,
                    price = price
                )
            return exist_product