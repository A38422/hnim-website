from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=12)
    price = models.IntegerField()
    image = models.CharField(max_length=255)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=5)
    type = models.CharField(max_length=20)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class AmountProductsCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    owner = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    @property
    def get_price(self):
        return self.product.price * self.amount


class Cart(models.Model):
    products = models.ManyToManyField(AmountProductsCart)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def get_bill(self):
        my_bill = 0
        amount_products = self.products.all()
        for amount_product in amount_products:
            my_bill += amount_product.product.price * amount_product.amount
        return my_bill


def validate_phone(value):
    if not re.match('(84|0[3|5|7|8|9])+([0-9]{8})', value):
        raise ValidationError(
            _('%(value)s is not phone number'),
            params={'value': value},
        )


class Transaction(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_paid = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, validators=[validate_phone])
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

