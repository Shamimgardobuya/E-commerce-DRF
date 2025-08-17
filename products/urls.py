from django.urls import path
from products.views import ProductApiView

urlpatterns = [
    path('', ProductApiView.as_view(),name="product-list"),
    path('/<int:pk>', ProductApiView.as_view(), name='product-detail'),
    path('<int:template>', ProductApiView.as_view()),

]
