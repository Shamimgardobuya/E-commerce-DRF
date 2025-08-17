from django.urls import path
from orders.views import OrderApiView

urlpatterns = [
    path('', OrderApiView.as_view(),name="orders"),
    path('/<int:pk>', OrderApiView.as_view(),name="order-detail")


]
