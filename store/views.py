from rest_framework import viewsets, mixins, generics
from django.shortcuts import render
from .models import Category, Product, ProductVariation, Cart, CartItem
from .serializers import CategorySerializer, ProductSerializer, ProductVariationSerializer, CartSerializer, CartItemSerializer

def home(request):
    return render(request, 'index.html')
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductListRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class ProductVariationListView(generics.ListAPIView):
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationSerializer   

class ProductVariationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationSerializer

class CartViewSet(mixins.CreateModelMixin, 
                  mixins.ListModelMixin, 
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin, 
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(mixins.CreateModelMixin, 
                      mixins.UpdateModelMixin, 
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer