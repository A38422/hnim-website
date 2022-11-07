from django.shortcuts import render
from .models import Product
from django.views import generic, View
from django.template import loader
from django.http import HttpResponse
# Create your views here.


def index(request):
    products = {
        'Products': Product.objects.all()
    }
    html_template = loader.get_template('product/index.html')
    return HttpResponse(html_template.render(products, request))
