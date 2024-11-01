from django.shortcuts import render, get_object_or_404
from django.http import Http404
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
from django.contrib.auth.models import User


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

    if not order_items:
        return Response({'error': 'Order items cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
    
    if any(item["quantity"] <= 0 for item in order_items):
        return Response({'error': 'Order items cannot have zero or negative quantities'}, status=status.HTTP_400_BAD_REQUEST)

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
            
            product_id = item["product"]

            
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                order.delete()
                raise Http404("Product not found")

            if product.stock < item['quantity']:
                print('i was here')
                order.delete()
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


@api_view(['POST'])
def stripe_webhook(request):
  
  webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, webhook_secret
    )
  except ValueError as e:
    return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
  except stripe.error.SignatureVerificationError as e:
    return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

  
  if event.type == 'checkout.session.completed':
     session = event['data']['object']

     line_items = stripe.checkout.Session.list_line_items(session['id'])
     price = session['amount_total']/100


     order = Order.objects.create(

        user = User(session.metadata.user),
        street = session.metadata.street,
        city = session.metadata.city,
        zip_code = session.metadata.zip_code,
        state=session.metadata.state,
        phone_no = session.metadata.phone_no,
        country = session.metadata.country,
        total_amount = price,
        payment_status="PAID",
     )

     for item in line_items['data']:


        line_product = stripe.Product.retrieve(item.price.product)
        product_id = line_product.metadata.product_id

        product = Product.objects.get(id=product_id)

        item = OrderItem.objects.create(
           
            product=product,
            order=order,
            name=product.name,
            quantity=item.quantity,
            price=item.price.unit_amount / 100,
            image= line_product.images[0]

        )
        
        product.stock -= item.quantity
        product.save()



     return Response({'details': 'payment successful'})
  