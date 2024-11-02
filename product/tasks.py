from celery import shared_task
import time
from .models import Product
from django.core.mail import send_mail
from restful_ecom.settings import EMAIL_HOST_USER

@shared_task
def notify_stock_to_admin(email):


    low_stock_products = Product.objects.filter(stock__lte=5)
    product_list = [
                {"product_id": product.id, "name": product.name, "stock": product.stock}
                                                        for product in low_stock_products
    ]
  

    body = f"Here is the list of low stock products\n {product_list}"
    recipients = [email]
    send_mail('Low Stock Alert',body,EMAIL_HOST_USER,recipients,fail_silently=False)