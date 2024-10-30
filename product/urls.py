from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path('products/', views.get_products, name="product"),
    path('products/upload_images/', views.upload_product_images, name="upload_product_images"),
    path('products/<str:pk>/', views.get_product_detail, name="product_detail"),
]
