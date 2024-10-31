from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from product.models import Product
from .serializers import OrderSerializer
from django.db import transaction
import stripe
import os
from utils.helpers import get_current_host

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def process_order(request, pk):
    with transaction.atomic():
        order = get_object_or_404(Order, pk=pk)
        order.status = request.data.get('status')
        order.save()
        serializer = OrderSerializer(order, many=False)
        return Response({'order': serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAdminUser,IsAuthenticated])
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    order.delete()

    return Response({'details': 'Order is deleted.'})





@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_orders(request):

    order = Order.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_single_order(request,pk):

    order = get_object_or_404(Order, pk=pk)
    serializer = OrderSerializer(order,many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):

    user = request.user
    data = request.data

    order_items = data['orderItems']

    if order_items and len(order_items)==0:
        return Response({'error': 'Order items cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

    else:

        total_amount = sum(item['price'] * item['quantity'] for item in order_items)
        
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            street = data['street'],
            city = data['city'],
            zip_code = data['zip_code'],
            state=data['state'],
            phone_no = data['phone_no'],
            country = data['country']
        )

        order_items_to_create = []

        for item in order_items:
            product = get_object_or_404(Product, id=item["product"])

            if product.stock < item['quantity']:
                return Response({'error': f'Not enough stock for {product.name}'}, status=status.HTTP_400_BAD_REQUEST)

            _items = OrderItem(
                product=product,
                order=order,
                name=product.name,
                quantity=item['quantity'],
                price=item['price']
            )

            order_items_to_create.append(_items)
            product.stock -= item['quantity']
            product.save()

        OrderItem.objects.bulk_create(order_items_to_create)

        serializer = OrderSerializer(order,many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


stripe.api_key = os.environ.get('STRIPE_PRIVATE_KEY')



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    DOMAIN =  get_current_host(request)
    user = request.user
    data = request.data

    order_items = data['orderItems']

    shipping_details= {
        'street': data['street'],
        'city': data['city'],
        'state': data['state'],
        'zip_code': data['zip_code'],
        'phone_no': data['phone_no'],
        'country': data['country'],
        'user': user.id
        
    }

    checkout_order_items = []

    for item in order_items:
        checkout_order_items.append({
            'price_data':{
                'currency': 'usd',
                'product_data': {
                    'name': item['name'],
                    'images': [item['image']],
                    'metadata': { "product_id": item['product']}
                },
                'unit_amount': item['price'] * 100
            },
                'quantity': item['quantity'],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        metadata= shipping_details,
        line_items= checkout_order_items,
        customer_email = user.email,
        mode='payment',
        success_url=DOMAIN,
        cancel_url=DOMAIN


    )

    return Response({'session': session}, status=status.HTTP_200_OK)