from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.db.models import Q
from apps.product.models import Product, Cart, AmountProductsCart, Transaction
import re


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
def filter_product(request, type):
    context = {'segment': 'index', 'Products': Product.objects.filter(type=type)}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def search_product(request, search):
    context = {'segment': 'index', 'Products': Product.objects.filter(
        Q(name__icontains=search) | Q(code__icontains=search)
    )}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def cart(request):
    queryset, created = Cart.objects.get_or_create(owner=request.user)
    context = {'carts': Cart.objects.filter(owner=request.user)}
    html_template = loader.get_template('home/cart/cart.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def add_cart(request, pk):
    context = {}

    if request.method == 'POST':
        user = request.user
        carts, created = Cart.objects.get_or_create(owner=user)

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Http404('Product does not exist')

        amount_product, created = AmountProductsCart.objects.get_or_create(product=product, owner=user)
        amount_product.amount = request.POST['amount']
        amount_product.save()
        carts.products.add(amount_product)
        carts.save()
        return redirect(reverse_lazy('cart'))
    html_template = loader.get_template('home/page-500.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url='/login/')
def remove_cart(request, pk):
    user = request.user
    cart, created = Cart.objects.get_or_create(owner=user)
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Http404('Product does not exist!')

    try:
        amount_product = AmountProductsCart.objects.get(product=product, owner=user)
    except AmountProductsCart.DoesNotExist:
        return Http404('Product does not exist in your cart!')

    amount_product.amount -= 1
    if amount_product.amount == 0:
        cart.products.remove(amount_product)
        cart.save()
    amount_product.amount = 0
    amount_product.save()
    cart.products.remove(amount_product)
    cart.save()

    return redirect(reverse_lazy('cart'))


@login_required(login_url='/login/')
def payment_view(request):
    context = {}
    html_template = loader.get_template('home/payments/payments.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url='/login/')
def submit_payment(request):
    context = {}
    html_template = loader.get_template('home/payments/payments.html')

    if request.method == 'POST':
        if not request.POST['fullname']:
            context = {'error': 'Vui lòng nhập họ tên!'}
            return HttpResponse(html_template.render(context, request))
        if not request.POST['address']:
            context = {'error': 'Vui lòng nhập địa chỉ!'}
            return HttpResponse(html_template.render(context, request))
        if not request.POST['phone']:
            context = {'error': 'Vui lòng nhập số điện thoại!'}
            return HttpResponse(html_template.render(context, request))
        elif not re.match('(84|0[3|5|7|8|9])+([0-9]{8})', request.POST['phone']):
            context = {'error': f'{request.POST["phone"]} không phải là số điện thoại!'}
            return HttpResponse(html_template.render(context, request))

        user = request.user
        transaction, created = Transaction.objects.get_or_create(owner=user)

        try:
            cart = Cart.objects.get(owner=user)
        except Cart.DoesNotExist:
            return Http404('Cart does not exist!')

        transaction.cart = cart
        transaction.owner = user
        transaction.is_paid = True
        transaction.fullname = request.POST['fullname']
        transaction.address = request.POST['address']
        transaction.phone = request.POST['phone']
        transaction.save()

        amount_products = AmountProductsCart.objects.all().filter(owner=user)
        for amount_product in amount_products:
            amount_product.amount = 0
            amount_product.save()
            cart.products.remove(amount_product)
            cart.save()

        html_template = loader.get_template('home/payments/payment_success.html')
        return HttpResponse(html_template.render(context, request))

    html_template = loader.get_template('home/page-500.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
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
