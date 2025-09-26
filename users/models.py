from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Покупатель'),
        ('manager', 'Менеджер'),
    )

    email = models.EmailField(unique=True, blank=False, null=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def is_customer(self):
        return self.role == 'customer'

    def is_manager(self):
        return self.role == 'manager'
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}"