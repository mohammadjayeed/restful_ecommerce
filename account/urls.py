from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
   
    path('register/', views.register, name="register"),
    path('me/', views.current_user_data, name="current_user"),


]
