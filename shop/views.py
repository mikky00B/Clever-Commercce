from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory


# Create your views here.
def home_view(request):
    latest_products = Product.objects.order_by("-created_at")[:8]

    featured_products = Product.objects.filter(discount_isnull=False).order_by(
        "-discount_discount_percentage"
    )[
        :4
    ]  # Show top 4 discounted products

    categories = ProductCategory.objects.all()

    # Context to pass to the template
    context = {
        "latest_products": latest_products,
        "featured_products": featured_products,
        "categories": categories,
    }

    return render(request, "home.html", context)


def search_view(request):
    query = request.GET.get("q")
    products = (
        Product.objects.filter(name__icontains=query)
        if query
        else Product.objects.all()
    )

    context = {
        "products": products,
        "query": query,
    }
    return render(request, "search_results.html", context)


def product_list_view(request, category_slug=None):
    category = None
    categories = ProductCategory.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(ProductCategory, slug=category_slug)
        products = products.filter(category=category)

    context = {
        "category": category,
        "categories": categories,
        "products": products,
    }
    return render(request, "product_list.html", context)


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    context = {
        "product": product,
    }
    return render(request, "product_detail.html", context)

def category_view(request, category_slug):
    category = get_object_or_404(ProductCategory, slug=category_slug)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category.html',context)