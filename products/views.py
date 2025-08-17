from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from registration.utils import RequiresScope
from categories.models import Category
from products.models import Product
from products.serializers import ProductSerializer
from categories.serializers import CategorySerializer
from rest_framework.response import Response
import pandas as pd
from django.http import HttpResponse
import io


# Create your views here.



class ProductApiView(APIView):
    @RequiresScope("create:products")
    def post(self, request, format=None):
        name = request.data.get("name")
        category_name = request.data.get("category")
        quantity = request.data.get("quantity")
        weight = request.data.get("weight")
        price = request.data.get("price")

        for key, value in category_name.items():
            find_category = Category.objects.filter(category_name=value).get()
            if find_category:
                product_exists, product = Product.objects.get_or_create(
                    name=name, category=find_category, quantity=quantity, weight=weight, price=price
                )
                data = ProductSerializer(product_exists)
                return Response(
                    {"message": f"Product created successfully, {data.data}"},
                    status=201,
                )
            return Response(
                {
                    "message": f"Category not found, here are the available{Category.objects.all()}"
                },
                status=201,
            )

    @RequiresScope("update:products")
    def put(self, request, pk=None):
        get_product = Product.objects.get(pk=pk)
        name = request.data.get("name")
        category_name = request.data.get("category")
        quantity = request.data.get("quantity")
        weight = request.data.get("weight")
        if get_product:
            for key, value in category_name.items():
                find_category = Category.objects.filter(category_name=value).get()
                if find_category:
                    get_product.name = name
                    get_product.category = find_category
                    get_product.quantity = quantity
                    get_product.weight = weight
                    
                    get_product.save()
                    data = ProductSerializer(get_product)
                    
                    return Response(
                        {
                            "message": f"Product updated successfully, {data.data}"
                        },
                        status=201,
                    )
                all_categories = CategorySerializer(Category.objects.all(), many=True)
                return Response(
                    {
                        "message": f"Category not found, here are the available{all_categories.data}"
                    },
                    status=201,
                )

    @RequiresScope("delete:products")
    def delete(self, request, pk):
        get_product = Product.objects.get(pk=pk)
        if get_product:
            get_product.delete()
            return Response({"message": "Product deleted successfully "}, status=200)
        return Response({"message": "Product not found successfully "}, status=400)

    @RequiresScope("read:products")
    def get(self, request, pk=None):
        if pk:
            find_product = ProductSerializer(Product.objects.get(pk=pk))
            return Response(
                {"message": f"Product fetched successfully, {find_product.data}"},
                status=200,
            )
        products = ProductSerializer(Product.objects.all(), many=True)
        return Response(
            {"message": f"Products fetched successfully, {products.data}"}, status=200
        )
