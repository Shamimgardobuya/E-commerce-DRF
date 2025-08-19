from django.urls import path
from products.views import ProductApiView, ProductListApiView

urlpatterns = [
    path('', ProductListApiView.as_view(),name="product-list"),
    path('<int:pk>', ProductApiView.as_view(), name='product-detail'),

]
