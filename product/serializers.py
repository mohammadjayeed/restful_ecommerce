from rest_framework import serializers
from .models import Product, ProductImages

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['name','description','price','rating','stock','images']

        extra_kwargs = {
            "name": {"required":True, "allow_blank":False}
        }

