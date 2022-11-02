from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=12)
    price = models.IntegerField()
    image = models.ImageField(upload_to='')
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=5)
    type = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


