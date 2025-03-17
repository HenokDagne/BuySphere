from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    
    ProductDetailView,
    login_view,
    filterViewSet,
    CategoryViewSet,
    HomeAPIView,
    ProductList,
    ProductListRetrieveUpdateView,
    ProductVariationListView,
    ProductVariationRetrieveUpdateDestroyView,
    CartViewSet,
    CartItemViewSet,
    ReviewCartView,
    CartView, 
    RemoveCartItemView,
    CheckoutView,
    OrderView,
)

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'order', OrderView, basename='order')

# Define the URL patterns for the generic views
urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', HomeAPIView.as_view(), name='home'),
    path('filter/<int:pk>/', filterViewSet.as_view(), name='filter'),
    path('', include(router.urls)),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductListRetrieveUpdateView.as_view(), name='product-retrieve-update'),
    path('product-variations/', ProductVariationListView.as_view(), name='product-variation-list'),
    path('product-variations/<int:pk>/', ProductVariationRetrieveUpdateDestroyView.as_view(), name='product-variation-retrieve-update-destroy'),
    path('create-cart/', CartView.as_view(), name='create-cart'),
    path('review-cart/', ReviewCartView.as_view(), name='review-cart'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    
    path('remove-item/', RemoveCartItemView.as_view(), name='remove_item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]

# Include the router URLs in the urlpatterns
urlpatterns += router.urls