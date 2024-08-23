from django.contrib import admin
from .models import Product, ProductImage, ProductCategory, Discount


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms displayed (can be set to 0)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image", "created_at"]


admin.site.register(Discount)
admin.site.register(ProductCategory)
