from django.urls import path
from . import views


app_name = "shop"

urlpatterns = [
    path("product/<slug:slug>/", views.product_detail_view, name="product_detail"),
    path(route="", view=views.home_view, name="home_view"),
]
