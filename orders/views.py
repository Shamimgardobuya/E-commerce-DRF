from django.shortcuts import render
from rest_framework.views import APIView
from registration.utils import RequiresScope
from datetime import datetime
from registration.models import Customer
from orders.models import Order
from  django.db.models import Sum
from products.models import Product
from orders.serializers import OrderSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from orders.sms_client import SendMessage
from django.conf import settings
from orders.email_orders import SendEmail
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class OrderApiView(APIView):
    @swagger_auto_schema(
            operation_description="Retrieves the specific order",
            responses={200:'Order fetched successfully.', 404: 'Order not found'}
    )
    @RequiresScope("read:orders")
    def get(self, request, pk=None):
        try:
            if pk:
                order = Order.objects.get(pk=pk)
                serialized = OrderSerializer(order, context={"request": request})
                return Response({
                        "message": "Order fetched successfully",
                        "data": serialized.data
                }, status=status.HTTP_200_OK)
            
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
            request_body=OrderSerializer,
            operation_description="Update an order",
            responses={200:'Order updated successfully.', 404: 'Order not found'}
    )
    @RequiresScope("update:orders")
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Order updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @RequiresScope("delete:orders")
    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


class OrderListApiView(APIView):
    @swagger_auto_schema(
            request_body=OrderSerializer,
            operation_description="Create an order",
            responses={201:'Order created successfully.', 400: 'Bad Request'}
    )
    @RequiresScope("create:orders")
    def post(self, request, format=None):
        try:
            find_user = Customer.objects.get(open_id=request.user.open_id)
            checkout = request.query_params.get("checkout")
            serializer = OrderSerializer(data = request.data, context={"request":request})
            if serializer.is_valid():
                serializer.save()  
                return Response(
                    {
                        "message": "Order created successfully",
                        "order": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    'checkout',
                    openapi.IN_QUERY,
                    description="Boolean value for completing orders",
                    type=openapi.TYPE_BOOLEAN
                ),
                
            ],
            operation_description="Retrieves all available orders for the customer",
            responses={200:'Order fetched successfully.', 404: 'Customer not found'}
    )
    @RequiresScope("read:orders")
    def get(self, request, pk=None, template=None):
        try:
            find_user = Customer.objects.get(open_id=request.user.open_id)
            checkout = request.query_params.get("checkout")
            if checkout:
                
                all_orders = Order.objects.filter(customer=find_user)


                sum_of_orders =  sum(order.total_price for order in all_orders)
                serialized_data = OrderSerializer(all_orders, many=True)

                orders_with_products = []
                for order in all_orders:
                    order_products = order.order_products.select_related('product').all()
                    orders_with_products.append({
                        'id': order.id,
                        'created_at': order.created_at,
                        'total_price': order.total_price,
                        'orderproduct': [
                            {
                                'product': {
                                    'name': op.product.name,
                                    'price': op.product.price
                                },
                                'quantity': op.quantity
                            }
                            for op in order_products
                        ]
                    })

                context = {
                    'customer': find_user.username,
                    'orders': orders_with_products,
                    'sum_of_orders': sum_of_orders,
                }

                send_sms = SendMessage(find_user.phone_number, context, settings.SMS_SHORT_CODE)
                send_sms.send()
                send = SendEmail(context=context)
                send.send_email()
                
                return Response({
                    "message": "Checked out orders  successfully",
                    "orders": serialized_data.data,
                    "total_price_sum": sum_of_orders
                }, status=status.HTTP_200_OK)
            orders = Order.objects.filter(customer=find_user)
            serialized_data = OrderSerializer(orders, many=True)
            return Response({
                "message": "Orders fetched successfully",
                "data": serialized_data.data
            }, status=status.HTTP_200_OK)
            
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Order not fetched {str(e)}"}, status=status.HTTP_404_NOT_FOUND)
    

            

    