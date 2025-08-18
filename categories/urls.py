from django.urls import path, include
from categories.views import CategoryApiView, CategoryListApiView
    
urlpatterns = [
    path('', CategoryListApiView.as_view(), name="category_list"),
    path('/<int:pk>', CategoryApiView.as_view(), name="category_detail")
]