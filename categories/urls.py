from django.urls import path, include
from categories.views import CategoryApiView
    
urlpatterns = [
    path('/<str:category>', CategoryApiView.as_view(), name="category-detail"),
    path('', CategoryApiView.as_view(), name="category"),
    path('<int:average_price>', CategoryApiView.as_view(), name="average_price"),



]
    