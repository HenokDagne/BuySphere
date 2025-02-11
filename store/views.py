from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView 
from django.shortcuts import render
from .models import Category, Product, ProductVariation, Cart, CartItem
from .serializers import CategorySerializer, ProductSerializer, ProductVariationSerializer, CartSerializer, CartItemSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
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

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_profile = request.user.profile
        cart, created = Cart.objects.create(user=user_profile, is_active=True)
        if not created and not cart.is_active:
            cart = Cart.objects.create(user=user_profile, is_active=True)
            cart.save()
        product_variation_id = request.data.get('product_variation_id')
        quantity = request.data.get('quantity', 1)
        product_variation = ProductVariation.objects.get(id=product_variation_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart,  productVariation=product_variation, quantity=quantity)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

class ReviewCartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_profile = request.user.profile
        cart = Cart.objects.get(user=user_profile, is_active=True)
        if not cart:
            return Response({'message': 'No active cart found'}, status=404)
        
        cart_items = CartItem.objects.filter(cart=cart)
        cart_serializer = CartSerializer(cart)
        cart_items_serializer = CartItemSerializer(cart_items, many=True)
        return Response({
            'cart': cart_serializer.data,
            'cart_items': cart_items_serializer.data
        })
    

    

            
        
        
        # create order from the cart items
        


class CartViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(mixins.CreateModelMixin, 
                      mixins.UpdateModelMixin, 
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer