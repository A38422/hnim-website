from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.http import Http404
from apps.product.models import Product, Cart, AmountProductsCart


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index', 'Products': Product.objects.all()}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def product_detail(request, pk):
    context = {'product': Product.objects.get(id=pk)}
    html_template = loader.get_template('home/product/product-detail.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def cart(request):
    context = {'carts': Cart.objects.all()}
    html_template = loader.get_template('home/cart/cart.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def add_cart(request, pk):
    user = request.user
    cart, created = Cart.objects.get_or_create(owner=user)

    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Http404('Product does not exist')

    amount_product, created = AmountProductsCart.objects.get_or_create(product=product, owner=user)
    amount_product.amount += 1
    amount_product.save()
    cart.products.add(amount_product)
    cart.save()
    return redirect('cart')


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
