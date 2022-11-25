from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('product-detail/<int:pk>', views.product_detail, name='product_detail'),

    path('cart/', views.cart, name='cart'),

    path('payment/', views.payment_view, name='payment'),

    path('submit-payment/', views.submit_payment, name='submit_payment'),

    path('add-cart/<int:pk>', views.add_cart, name='add_cart'),

    path('remove-cart/<int:pk>', views.remove_cart, name='remove_cart'),

    re_path(r'^products/(?P<type>\w{0,50})/$', views.filter_product, name='filter_product'),

    re_path(r'^.*\.*', views.pages, name='pages'),


]
