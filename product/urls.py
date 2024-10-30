from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path('products/', views.get_products, name="product"),
    path('products/<str:pk>/', views.get_product_detail, name="product_detail"),
]
