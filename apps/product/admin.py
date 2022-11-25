from django.contrib import admin
from .models import Product, Cart, AmountProductsCart, Transaction

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price')


class CartAdmin(admin.ModelAdmin):
    list_display1 = ('products', 'owner')


class AmountProductsCartAdmin(admin.ModelAdmin):
    list_display2 = ('product', 'owner')


class TransactionAdmin(admin.ModelAdmin):
    list_display3 = ('cart', 'fullname', 'address', 'is_paid', 'owner')


admin.site.register(Product, ProductAdmin)

admin.site.register(Cart, CartAdmin)

admin.site.register(AmountProductsCart, AmountProductsCartAdmin)

admin.site.register(Transaction, TransactionAdmin)
