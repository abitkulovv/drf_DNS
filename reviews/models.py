from django.db import models
from django.conf import settings
from catalog.models import Product


User = settings.AUTH_USER_MODEL


class Review(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('approved', 'Одобрен'),
        ('rejected', 'Отклонён'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # 1-5
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  

    def __str__(self):
        return f"{self.user.username} -> {self.product.name} ({self.status})"