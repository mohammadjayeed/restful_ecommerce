from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, ProductImages
from .serializers import ProductSerializer, ProductImageSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# Create your views here.


@api_view(['POST', 'GET'])
def list_create_products(request):
    if request.method == 'POST': # create operation
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'product': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # Get products
        products = Product.objects.all()
        # count = products.count()
        result_per_page = 2

        paginator = PageNumberPagination()
        paginator.page_size = result_per_page
        queryset = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(queryset, many=True)
        return paginator.get_paginated_response({
            'result_per_page': result_per_page,
            'products': serializer.data
        })

@api_view(['GET','PUT','DELETE'])
def get_product_detail(request,pk):

    product = get_object_or_404(Product,pk=pk)

    if request.method == "GET": #retrieve operation

        serializer = ProductSerializer(product) 
        return Response({'product':serializer.data},status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = ProductSerializer(product,data=request.data) # update operation
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def upload_product_images(request,pk):
    product_id = pk
    files = request.FILES.getlist('images')

    images = []

    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    for f in files:
        image = ProductImages.objects.create(product=product, image=f)
        images.append(image)
    
    serializer = ProductImageSerializer(images, many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)



