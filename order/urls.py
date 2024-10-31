from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path('orders/place/', views.place_order, name="place_order"),
    path('orders/', views.get_orders, name="get_orders"),
    path('orders/<str:pk>/', views.get_single_order, name="get_single_order"),

]
