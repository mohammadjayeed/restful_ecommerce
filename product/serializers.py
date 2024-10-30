from rest_framework import serializers
from .models import Product, ProductImages


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','description','price','rating','stock']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"