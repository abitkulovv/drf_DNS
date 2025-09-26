from rest_framework import serializers
from .models import Cart, CartItem, PromoCode
from catalog.serializers import ProductSerializer
from catalog.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),  
        write_only=True,
        source='product',  
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'subtotal']



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_after_discount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    promo_code = serializers.CharField(source='promo.code', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total', 'total_after_discount', 'promo_code']



class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'
