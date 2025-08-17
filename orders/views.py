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


class OrderApiView(APIView):

    @RequiresScope("create:orders")
    def post(self, request, format=None):
        try:
            serializer = OrderSerializer(data = request.data, context={"request":request})
            # print("yopop"*50, serializer)
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
                # Return validation errors if not valid
                return Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @RequiresScope("read:orders")
    def get(self, request, pk=None, template=None):
        try:
            find_user = Customer.objects.get(open_id=request.user.open_id)
            checkout = request.query_params.get("checkout")
            print("checkout", checkout)
            if checkout:
                
                all_orders = Order.objects.filter(customer=find_user)


                sum_of_orders =  sum(order.total_price for order in all_orders)
                serialized_data = OrderSerializer(all_orders, many=True)
                # print("<>"*100, serialized_data)

                # print("<"*100, serialized_data)

                context = {
                        'customer': find_user.username,        
                        'orders': all_orders,                
                        'sum_of_orders': sum_of_orders,       
                    }
                # print("<"*100, context)

                # SendMessage(find_user.phone_number, context, settings.SMS_SHORT_CODE )

                send = SendEmail(context=context)
                send.send_email()
                
                return Response({
                    "message": "Checked out orders  successfully",
                    "orders": serialized_data.data,
                    "total_price_sum": sum_of_orders['total_sum']
                }, status=status.HTTP_200_OK)

            if pk:
                order = Order.objects.get(pk=pk)
                serialized = OrderSerializer(order, data = request.data, context={"request", request})
                if serialized.is_valid():
                    serialized.save()
                    return Response({
                        "message": "Order fetched successfully",
                        "data": serialized_data.data
                    }, status=status.HTTP_200_OK)

            orders = Order.objects.select_related("customer").filter(customer=find_user)
            serialized_data = OrderSerializer(orders, many=True)
            return Response({
                "message": "Orders fetched successfully",
                "data": serialized_data.data
            }, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Order not fetched {str(e)}"}, status=status.HTTP_404_NOT_FOUND)
    
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



# @api_view(['POST', 'GET'])
# @permission_classes([AllowAny])
# def incoming_messages(request):
#     try:
#         data = request.get_json(force=True)
#         print(f"Incoming message...\n ${data}")
#         return Response(status=200)
#     except Exception as e:
#         return Response({"message": f"Error occurred {str(e)}"})

