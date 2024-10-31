from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path('orders/', views.place_order, name="place_order"),

]
