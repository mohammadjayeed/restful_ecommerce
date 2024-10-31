from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path('products/', views.list_create_products, name="product"),
    path('products/<str:pk>/', views.get_product_detail, name="product_detail"),
    path('products/<str:pk>/review/', views.create_delete_review, name="product_review"),
    path('products/<str:pk>/upload_images/', views.upload_product_images, name="upload_product_images"),
]
