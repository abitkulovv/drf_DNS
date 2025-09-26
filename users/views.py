from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User, Address
from .serializers import RegisterSerializer, ProfileSerializer, AddressSerializer



class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        address = self.get_object()  
        if address.order_set.exists():  
            return Response(
                {"error": "This address is used in your orders"},
                status=status.HTTP_400_BAD_REQUEST  
            )
        return super().destroy(request, *args, **kwargs)  