from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'created_at']  


    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("The rating must be from 1 to 5")
        return value
    
    def validate(self, data):
        user = self.context['request'].user
        product = data['product']
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already left a review for this product.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)