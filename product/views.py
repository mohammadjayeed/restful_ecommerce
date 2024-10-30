from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from .models import Product, ProductImages
from .serializers import ProductSerializer, ProductImageSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# Create your views here.

@api_view(['GET'])
def get_products(request):

    products = Product.objects.all()

    count = products.count()
    result_per_page = 2

    paginator = PageNumberPagination()
    paginator.page_size = result_per_page

    queryset = paginator.paginate_queryset(products,request)

    serializer = ProductSerializer(queryset, many=True)

    return Response({
        'sitewide_products_available': count,
        'result_per_page': result_per_page,
        'products':serializer.data
        })

@api_view(['GET'])
def get_product_detail(request,pk):

    product = get_object_or_404(Product,pk=pk)

    serializer = ProductSerializer(product, many=False)

    return Response({'product':serializer.data})




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

    return Response(serializer.data)



