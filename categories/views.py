from django.shortcuts import render
from rest_framework.views import APIView
from registration.utils import RequiresScope, FindAverageProduct
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.response import Response
import pandas as pd 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 
from rest_framework import status
# Create your views here.


class CategoryApiView(APIView):
    
    @swagger_auto_schema(
        request_body=CategorySerializer,
        operation_description="Updates a category",
        responses={200:'Category updated successfully.', 404: 'Category not found'}
    )
    @RequiresScope("update:categories")
    def put(self, request, pk, format=None):
        try:
            if pk:
                category = request.data.get("category_name")
                parent = request.data.get("parent_category")
                existed,new_parent_category = Category.objects.get_or_create(category_name = parent)
                find_category = Category.objects.get(pk=pk)
                
                if find_category and category:
                    find_category.category_name = category
                    find_category.parent = existed

                    find_category.save()
                data = CategorySerializer(find_category)
                return Response(
                    {"message": "Category updated successfully", "data": data.data}, status=200
                )
        
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'average_price',
                openapi.IN_QUERY,
                description="Boolean value for calculating average price, involves getting all products linked to their products and getting average",
                type=openapi.TYPE_BOOLEAN
            ),
            
        ],
        operation_description="Retrieves a specific category",
        responses={200:"Category fetched successfully.", 404: "Category not found"}
    )
    @RequiresScope("read:categories")
    def get(self, request,pk=None,format=None):
        average_price = request.query_params.get("average_price")
        category_object = Category.objects.get(pk=pk)

        if average_price and category_object:
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
    
    
    @swagger_auto_schema(
            operation_description="Deletes a category",
            responses={200:'Category deleted successfully.', 404: 'Category does not exist'}
    )
    @RequiresScope("delete:categories")
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({"message": f"Category deleted successfully"}, 200)
    
        except Category.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
            

class CategoryListApiView(APIView):
        
    @swagger_auto_schema(
            request_body=CategorySerializer,
            operation_description="Create a category",
            responses={201:'Category created successfully.', 400: 'Bad request'}
    )
    @RequiresScope("create:categories")
    def post(self,request):
        try:
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
                    message = {"Category created successfully": data.data}
                    return Response(message, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({message: "Bad request"}, status.HTTP_400_BAD_REQUEST)

        
    @swagger_auto_schema(
        operation_description="Retrieves categories",
        responses={200:"Categories fetched successfully.", 404: "Category not found"}
    )
    def get(self, request,format=None):
        try:
            categories = CategorySerializer(Category.objects.all(), many=True)
            return Response(
                {"message": f"Categories fetched successfully, {categories.data}"}, status=200
            )

        except Exception as e:
            return Response(
                {"message": f"Error occurred, {str(e)}"},status=500
            )
    