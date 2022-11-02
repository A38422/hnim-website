from django.shortcuts import render
from .models import Product
from django.views import generic, View
from django.template import loader
from django.http import HttpResponse
# Create your views here.


# def list(request):
#     Data = {
#         'Products': Product.objects.all().order_by('-date')
#     }
#     return render(request, '')

class ProductsView(generic.ListView):
    model = Product

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user'] = self.request.user
        return context


def index(request):
    products = {
        'Products': Product.objects.all()
    }
    html_template = loader.get_template('product/index.html')
    return HttpResponse(html_template.render(products, request))
