from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import CategoryViewSet, ProductViewSet, ProductVariationViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'variations', ProductVariationViewSet)

urlpatterns = [
      path('', views.home, name='home'),
      path('', include(router.urls)),
]