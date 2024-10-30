from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100,default="",blank=False)
    description = models.TextField(max_length=1000, default="", blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # Will add User Profile later
    # Will add image later
    # Will add review later