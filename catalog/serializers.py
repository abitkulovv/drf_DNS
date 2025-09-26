from rest_framework import serializers

from .models import Category, Product
from reviews.models import Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'rating', 'comment']



class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'reviews', 'average_rating']

    def get_reviews(self, obj):
        approved_reviews = obj.reviews.filter(status='approved')
        return ProductReviewSerializer(approved_reviews, many=True).data

    def get_average_rating(self, obj):
        approved_reviews = obj.reviews.filter(status='approved')
        if not approved_reviews.exists():
            return None
        return round(sum(r.rating for r in approved_reviews) / approved_reviews.count(), 2)