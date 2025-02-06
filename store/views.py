from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView 
from django.shortcuts import render
from .models import Category, Product, ProductVariation, Cart, CartItem
from .serializers import CategorySerializer, ProductSerializer, ProductVariationSerializer, CartSerializer, CartItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class HomeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        categories = Category.objects.all()
        product_serializer = ProductSerializer(products, many=True, context={'request': request})
        category_serializer = CategorySerializer(categories, many=True, context={'request': request})
        return render(request, 'index.html' , {
            'products': product_serializer.data, 
            'categories': category_serializer.data
        })
    
class filterViewSet(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        product = Product.objects.filter(category_id=pk)
        filtered_products = ProductSerializer(product, many=True, context={'request': request})
        return Response({'category': CategorySerializer(category, context={'request': request}).data, 'products': filtered_products.data})

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