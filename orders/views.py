from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer
from users.permissions import IsOwnerOrManager

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrManager]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        order = self.get_object()
        if order.status != 'new':
            return Response({"detail": "Can't pay for this order"}, status=status.HTTP_400_BAD_REQUEST)

        
        if order.user != request.user and request.user.role != 'manager':
            return Response({"detail": "No access"}, status=status.HTTP_403_FORBIDDEN)

        order.status = 'paid'
        order.save()
        return Response({"detail": "The order is paid", "status": order.status})