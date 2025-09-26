from rest_framework import serializers
from decimal import Decimal

from .models import Order, OrderItem
from users.models import Address
from cart.models import Cart


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'get_total']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), write_only=True, source='address'
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'address_id', 'status', 'total', 'items', 'created_at']
        read_only_fields = ['user', 'status', 'total', 'address']

    def create(self, validated_data):
        user = self.context['request'].user
        address = validated_data['address']
        cart = Cart.objects.get(user=user)

        if not cart.items.exists():
            raise serializers.ValidationError("Cart is empty")


        if hasattr(cart, 'promo') and cart.promo and cart.promo.is_valid():
            discount = Decimal(cart.promo.discount_percent) / Decimal('100')
            total = (cart.total * (Decimal('1') - discount)).quantize(Decimal('0.01'))
        else:
            total = cart.total

        order = Order.objects.create(
            user=user,
            address=address,
            total=total
        )

        for item in cart.items.all():
            if item.quantity > item.product.stock:
                raise serializers.ValidationError(f"Not enough in stock: {item.product.name}")
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            
            item.product.stock -= item.quantity
            item.product.save()

        
        cart.items.all().delete()

        return order
