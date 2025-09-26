from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
from .utils import send_order_update_email

@receiver(pre_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    if not instance.pk:
        return 

    old_status = Order.objects.get(pk=instance.pk).status
    if instance.status != old_status:
        send_order_update_email(instance)