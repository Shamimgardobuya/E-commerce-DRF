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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 
from rest_framework import status

# Create your views here.



class ProductApiView(APIView):
    @swagger_auto_schema(
            request_body=ProductSerializer,
            operation_description="Updates a product",
            responses={200:'Product updated successfully.', 400: 'Invalid request'}
    )
    @RequiresScope("update:products")
    def put(self, request, pk=None):
        try:
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
                            status=status.HTTP_200_OK,
                        )
        except Exception as e:
            return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
        
                
    @swagger_auto_schema(
        operation_description="Deletes a specific product",
        responses={200: "Product fetched successfully", 404: "Product not found"}
    )
    @RequiresScope("delete:products")
    def delete(self, request, pk):
        get_product = Product.objects.get(pk=pk)
        if get_product:
            get_product.delete()
            return Response({"message": "Product deleted successfully "}, status=status.HTTP_200_OK)
        return Response({"message": "Product not found "}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Retrieves a product",
        responses={200: "Product fetched successfully", 404: "Product not found"}
    )
    @RequiresScope("read:products")
    def get(self, request, pk=None):
        try:
            if pk:
                find_product = ProductSerializer(Product.objects.get(pk=pk))
                return Response(
                    {"message": "Product fetched successfully",  "data":find_product.data},
                    status=200,
                )

        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
        

class ProductListApiView(APIView):
    @swagger_auto_schema(
            request_body=ProductSerializer,
            operation_description="Create a product",
            responses={201:'Product created successfully.', 400: 'Product not creates'}
    )
    @RequiresScope("create:products")
    def post(self, request):
        serialized_product = ProductSerializer(data=request.data)

        if serialized_product.is_valid():
            serialized_product.save()
            return Response(
                {"message": f"Product created successfully, {serialized_product.data}"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": f"Product not created, {serialized_product.errors}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
                
    @swagger_auto_schema(
        operation_description="Retrieves all available products",
        responses={200: "Products fetched successfully", 500: "Error occurrred"}
    )
    @RequiresScope("read:products")
    def get(self,request):
        try:
            products = ProductSerializer(Product.objects.all(), many=True)

            return Response(
                {"message": "Products fetched successfully", "data": products.data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
