from django.shortcuts import render
from rest_framework.views import APIView
from registration.utils import RequiresScope, FindAverageProduct
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.response import Response
import pandas as pd 

# Create your views here.
  

class CategoryApiView(APIView):
    @RequiresScope("create:categories")
    def post(self, request, format=None):
        category = request.data.get("category_name")
        parent_category = request.data.get("parent_category")
        if category:
            category_exists, create_category = Category.objects.get_or_create(
                category_name=parent_category
            )
            child_category_exists, create_child_category = (
                Category.objects.get_or_create(
                    category_name=category, parent=category_exists
                )
            )
            data = CategorySerializer(child_category_exists)
            message = {"Category created successfully": data.data}, 201
        else:
            message = {"You have not provided the category"}, 400

        return Response(message)

    @RequiresScope("update:categories")
    def put(self, request, pk, format=None):
        if pk:
            category = request.data.get("category_name")
            parent = request.data.get("parent_category")

            # print(category.items())
            find_category = Category.objects.get(pk=pk)
            if find_category and category:
                find_category.category_name = category
                find_category.parent = parent

                find_category.save()
            data = CategorySerializer(find_category)
            return Response(
                {"message": "Category updated successfully", "data": data.data}, status=201
            )
    @RequiresScope("read:categories")
    def get(self, request,category=None,format=None):
        average_price = request.query_params.get("average_price")
        category = category.title()
        category_object = Category.objects.filter(category_name=category).get()

        if average_price and category:
            average_data = FindAverageProduct(category_object.id)
            average_price = average_data.create_view()
            if average_price:
                return Response(
                    {"message": f"Average price fetched successfully", "data": average_price}, status=200
                )
                
        if category_object:
            find_category = CategorySerializer(Category.objects.get(pk=category_object.id))
            return Response(
                {"message": f"Category fetched successfully, {find_category.data}"}, status=200
            )
        
        categories = CategorySerializer(Category.objects.all(), many=True)
        return Response(
            {"message": f"Categories fetched successfully, {categories.data}"}, 200
        )

    @RequiresScope("delete:categories")
    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response({"message": f"Category deleted successfully"}, 200)
