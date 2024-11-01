from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path('orders/place/', views.place_order, name="place_order"),
    path('orders/webhook/', views.stripe_webhook, name="stripe_webhook"),
    path('orders/', views.get_orders, name="get_orders"),
    path('orders/<str:pk>/', views.get_single_order, name="get_single_order"),
    path('orders/<str:pk>/process/', views.process_order, name="process_order"),
    path('orders/<str:pk>/delete/', views.delete_order, name="delete_order"),

    path('create-checkout-session/', views.create_checkout_session, name="create_checkout_session"),


]
