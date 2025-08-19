from django.urls import path
from orders.views import OrderApiView, OrderListApiView

urlpatterns = [
    path('', OrderListApiView.as_view(),name="orders-list"),
    path('<int:pk>', OrderApiView.as_view(),name="order-detail")


]
