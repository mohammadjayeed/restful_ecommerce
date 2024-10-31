from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100,default="",blank=False)
    description = models.TextField(max_length=1000, default="", blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True,related_name="images")
    image = models.ImageField(upload_to="products",blank=True,null=True)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(default="", blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment)