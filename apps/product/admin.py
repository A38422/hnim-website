from django.contrib import admin
from .models import Product

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price')


admin.site.register(Product, ProductAdmin)