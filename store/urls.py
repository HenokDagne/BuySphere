
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HomeAPIView,
    CategoryViewSet,
    ProductList,
    ProductListRetrieveUpdateView,
    ProductVariationListView,
    ProductVariationRetrieveUpdateDestroyView,
    CartViewSet,
    CartItemViewSet
)

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

# Define the URL patterns for the generic views
urlpatterns = [
    path('home/', HomeAPIView.as_view(), name='home'),
    path('', include(router.urls)),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductListRetrieveUpdateView.as_view(), name='product-retrieve-update'),
    path('product-variations/', ProductVariationListView.as_view(), name='product-variation-list'),
    path('product-variations/<int:pk>/', ProductVariationRetrieveUpdateDestroyView.as_view(), name='product-variation-retrieve-update-destroy'),
]

# Include the router URLs in the urlpatterns
urlpatterns += router.urls

