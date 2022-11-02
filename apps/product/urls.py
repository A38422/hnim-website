from django.urls import path

from apps.product import views

urlpatterns = [
    path("product/", views.index),
]
