# cart/models.py
from django.db import models
from django.conf import settings

from django.utils import timezone
from decimal import Decimal

from catalog.models import Product


User = settings.AUTH_USER_MODEL


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField()  
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.expires_at > timezone.now()

    def __str__(self):
        return f"{self.code} ({self.discount_percent}% off)"



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    promo = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def total_after_discount(self):
        if self.promo and self.promo.is_valid():
            discount = Decimal(self.promo.discount_percent) / Decimal('100')
            return (self.total * (Decimal('1') - discount)).quantize(Decimal('0.01'))
        return self.total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def subtotal(self):
        return self.product.price * self.quantity




