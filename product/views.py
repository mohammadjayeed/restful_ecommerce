from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Product, ProductImages, Review
from .serializers import ProductSerializer, ProductImageSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsAdminUserForPost, IsAdminUserForUpdateDelete
from order.models import OrderItem
# Create your views here.


@api_view(['POST', 'GET'])
@permission_classes([IsAdminUserForPost])
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
@permission_classes([IsAdminUserForUpdateDelete])
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
@permission_classes([IsAuthenticated, IsAdminUser])
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



@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def create_delete_review(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)

    order_items_with_product = OrderItem.objects.filter(order__user=user, product=product)
    
    
    if not order_items_with_product.exists():
        return Response({'error': 'You need to have purchased this product to review it.'},
                        status=status.HTTP_403_FORBIDDEN)
    
    
    paid_order = order_items_with_product.filter(order__payment_status="PAID").exists()
    
    if not paid_order:
        return Response({'error': 'You cannot review the product until a payment has been made.'},
                        status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'POST':
        data = request.data
        review = product.reviews.filter(user=user)

        if review.exists():
            
            review.update(comment=data['comment'])
            return Response({'message': 'Review updated'}, status=status.HTTP_200_OK)

        
        Review.objects.create(
            user=user,
            product=product,
            comment=data['comment']
        )
        return Response({'message': 'Review created'}, status=status.HTTP_201_CREATED)

    
    elif request.method == 'DELETE':
        review = product.reviews.filter(user=user)

        if review.exists():
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)