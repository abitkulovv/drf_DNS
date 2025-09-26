from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet



categories_router = DefaultRouter()
categories_router.register(r'', CategoryViewSet)

products_router = DefaultRouter()
products_router.register(r'', ProductViewSet)

urlpatterns = [
    path('categories/', include(categories_router.urls)),
    path('products/', include(products_router.urls)),
]