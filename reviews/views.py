from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            return Review.objects.all() 
        return Review.objects.filter(user=user)  


    def _change_status(self, review, new_status):
        if self.request.user.role != 'manager':
            return Response({'detail': 'No access'}, status=status.HTTP_403_FORBIDDEN)
        review.status = new_status
        review.save()
        return Response({'detail': f'New status: {new_status}'}, status=status.HTTP_202_ACCEPTED)


    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        review = self.get_object()
        return self._change_status(review, 'approved')


    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        review = self.get_object()
        return self._change_status(review, 'rejected')