from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Cart, CartItem, Order, OrderItem
from shop.models import Product


# Create your views here.


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        "cart": cart,
        "cart_items": cart.items.all(),
        "total_price": cart.get_total_price(),
    }
    return render(request, "cart/view_cart.html", context)


def add_to_cart(request, product_id):
    if (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):  # Check if the request is an AJAX request
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse(
            {
                "status": "success",
                "message": "Product added to cart",
                "total_items": cart.items.count(),
            }
        )
    else:
        return HttpResponseBadRequest("Invalid request")


@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease":
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                return redirect("view_cart")

        cart_item.save()

    return redirect("view_cart")


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect("view_cart")


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    if cart.items.count() == 0:
        return redirect("view_cart")  # Redirect to cart if it's empty

    order = Order.objects.create(
        customer=request.user,
        # shipping_address="Shipping Address",  # Get this from user input
        # billing_address="Billing Address",  # Get this from user input
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    cart.items.all().delete()  # Clear the cart after checkout

    return redirect("view_order", order_id=order.id)


@login_required
def view_orders(request):
    orders = Order.objects.filter(customer=request.user)
    context = {"orders": orders}
    return render(request, "orders/view_orders.html", context)


@login_required
def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    context = {
        "order": order,
        "order_items": order.items.all(),
        "total_price": order.get_total_price(),
    }
    return render(request, "orders/view_order.html", context)
