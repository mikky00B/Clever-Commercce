from django.urls import path
from . import views


urlspatterns = [
    path("product/<slug:slug>/", views.product_detail, name="product_detail")
]
