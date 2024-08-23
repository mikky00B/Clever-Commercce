from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderItem, Order


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    order.total_price = order.get_total_price()
    order.save()
