from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
@api_view(['POST'])
def register(request):

    user = SignUpSerializer(data= request.data)

    if user.is_valid():
        if not User.objects.filter(username=request.data['username']).exists():
            user_data = {
                
                "username" : request.data['username'],
                "email" : request.data['email'],
                "first_name": request.data.get('first_name'), 
                "last_name": request.data.get('last_name'), 
                "password" : make_password(request.data['password']),
                "is_staff": request.data.get("is_staff")


            }
            user = User.objects.create(**user_data)
            user.save()
            return Response({"message":"User Registered"}, status=status.HTTP_201_CREATED)


        else:
            return Response({"error":"User exists"}, status=status.HTTP_400_BAD_REQUEST)


    else:
        return Response({"errors": user.errors}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_data(request):

    user = UserSerializer(request.user)
    return Response(user.data, status=status.HTTP_200_OK)