from django.urls import path, re_path
from . import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # The product detail
    path('product-detail/<int:pk>', views.product_detail, name='product_detail'),

    # The cart
    path('cart/', views.cart, name='cart'),

    path('add_cart/<int:pk>', views.add_cart, name='add_cart'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
