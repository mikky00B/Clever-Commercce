from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver
from django.urls import reverse


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        "ProductCategory", on_delete=models.CASCADE, related_name="products"
    )
    inventory = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.ForeignKey(
        "Discount", on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

    def get_discounted_price(self):
        """
        Returns the price after applying the discount.
        """
        if self.discount and self.discount.active:
            return self.price * (1 - self.discount.discount_percentage / 100)
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.name)
            slug = original_slug
            counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.product.name} Image"


class Discount(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.name


@receiver(pre_save, sender=ProductCategory)
def addslug_to_product_category(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)
