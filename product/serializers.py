from rest_framework import serializers
from .models import Product, ProductImages, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields= "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField(method_name='get_reviews',read_only=True)

    class Meta:
        model = Product
        fields = ['id','name','description','price','stock','images','reviews']

        extra_kwargs = {
            "name": {"required":True, "allow_blank":False}
        }

    def get_reviews(self,obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews,many=True)
        return serializer.data
