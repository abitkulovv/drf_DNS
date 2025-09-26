from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem, PromoCode
from .serializers import CartSerializer, CartItemSerializer
from catalog.models import Product

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart


    def list(self, request):
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if created:
            if quantity > product.stock:
                return Response({'error': f'Not enough stock. Only {product.stock} left.'}, status=status.HTTP_400_BAD_REQUEST)
            item.quantity = quantity
        else:
            new_quantity = item.quantity + quantity
            if new_quantity > product.stock:
                return Response({'error': f'Not enough stock. Only {product.stock} left.'}, status=status.HTTP_400_BAD_REQUEST)
            item.quantity = new_quantity

        item.save()
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    @action(detail=True, methods=['patch'])
    def update_quantity(self, request, pk=None):
        cart = self.get_cart(request.user)
        try:
            item = CartItem.objects.get(cart=cart, id=pk)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        quantity = int(request.data.get('quantity', 1))
        if quantity > item.product.stock:
            return Response({'error': f'Not enough stock. Only {item.product.stock} left.'}, status=status.HTTP_400_BAD_REQUEST)

        item.quantity = quantity
        item.save()
        serializer = CartItemSerializer(item)
        return Response(serializer.data)

    
    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        cart = self.get_cart(request.user)
        try:
            item = CartItem.objects.get(cart=cart, id=pk)
            item.delete()
            return Response({'success': 'Item removed'})
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    
    @action(detail=False, methods=['post'])
    def apply_promo(self, request):
        cart = self.get_cart(request.user)
        code = request.data.get('code', '').strip()

        try:
            promo = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            return Response({'error': 'Promo code not found'}, status=status.HTTP_404_NOT_FOUND)

        if not promo.is_valid():
            return Response({'error': 'Promo code expired'}, status=status.HTTP_400_BAD_REQUEST)

        cart.promo = promo
        cart.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
