from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.view_orders, name="view_orders"),
    path("orders/<int:order_id>/", views.view_order, name="view_order"),
]
