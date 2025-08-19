
from rest_framework import serializers
from products.models import Product
from categories.models import Category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.DictField(
        write_only=True,
        help_text="Provide category as {'Parent': 'Child'}"
    )
    class Meta:
        model = Product
        fields = ("category", "name", "quantity", "weight", "units", "price")

    def validate_units(self, value):
        units_ = ['grams','kilograms','milliliters','liters']
        if value not in units_:
            raise serializers.ValidationError(
                f"Units of product needs to be either one of these {units_}"
            )
        return value

    def validate_category(self, value):
        if not isinstance(value, dict) or len(value) != 1:
            raise serializers.ValidationError("Category must be in form {'parent': 'child'}")

        parent_name, child_name = list(value.items())[0]

        try:
            parent_category = Category.objects.get(category_name=parent_name, parent=None)
        except Category.DoesNotExist:
            raise serializers.ValidationError(f"Parent category '{parent_name}' does not exist.")

        try:
            child_category = Category.objects.get(category_name=child_name, parent=parent_category)
        except Category.DoesNotExist:
            raise serializers.ValidationError(
                f"Child category '{child_name}' does not exist under '{parent_name}'."
            )

        return child_category 

    def create(self, validated_data):
        category = validated_data.pop("category")
        return Product.objects.create(category=category, **validated_data)