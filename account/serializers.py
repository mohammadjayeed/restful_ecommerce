from rest_framework import serializers
from django.contrib.auth.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','is_staff','password')

        extra_kwargs = {

            'username': {'required':True, "allow_blank":False},
            'email': {'required':True, "allow_blank":False},
            'password': {'required':True, "allow_blank":False, 'min_length':4},
            'first_name': {'required': True, 'allow_blank':False},  
            'last_name': {'required': True, 'allow_blank':False}, 
            'is_staff': {'required': True},  


        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')