from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, ProductVariation, Cart, CartItem
from .serializers import CategorySerializer, ProductSerializer, ProductVariationSerializer, CartSerializer, CartItemSerializer
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm # Django uses AuthenticationForm to validate the username and password.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


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
    


class ProductDetailView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        try:
            product = get_object_or_404(Product, id=pk)
            product_variations = ProductVariation.objects.filter(product=product)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        except ProductVariation.DoesNotExist:
            return Response({'error': 'Product variations not found'}, status=404)

        product_serializer = ProductSerializer(product, context={'request': request})
        product_variations_serializer = ProductVariationSerializer(product_variations, many=True, context={'request': request})

        return render(request, 'productdetail.html', {
            'product': product_serializer.data,
            'product_variations': product_variations_serializer.data
        })
        

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
        cart, created = Cart.objects.get_or_create(user=user_profile, is_active=True)
        if not created and not cart.is_active:
            cart = Cart.objects.create(user=user_profile, is_active=True)
            cart.save()
        
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        # Filter ProductVariation related to the given product_id and select the first one
        product_variation = ProductVariation.objects.filter(product_id=product_id).first()
        
        if not product_variation:
            return Response({'message': 'No product variation found for the given product ID'}, status=404)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, productVariation=product_variation)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        return Response({'message': 'Item added to cart', 'cart_item_id': cart_item.id})


class RemoveCartItemView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_profile = request.user.profile
        cart = Cart.objects.filter(user=user_profile, is_active=True).first()
        if not cart:
            return Response({'message': 'No active cart found'}, status=404)
        
        cart_item_id = request.data.get('cart_item_id')
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
        cart_item.delete()

        return Response({'message': 'Item removed from cart'})    


    
class ReviewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_profile = request.user.profile
        cart = Cart.objects.filter(user=user_profile, is_active=True).first()
        if not cart:
            return Response({'message': 'No active cart found'}, status=404)
        

        cart_items = CartItem.objects.filter(cart=cart).select_related('productVariation__product')
        
        cart_serializer = CartSerializer(cart, context={'request': request})
        
        cart_items_serializer = CartItemSerializer(cart_items, many=True, context={'request': request})
        return render(request, 'cart.html', {
            'cart': cart_serializer.data,
            'cart_items': cart_items_serializer.data
        })
   

    

def review_cart(request):
    return render(request, 'cart.html')            
# create order from the cart items
        
class CartViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

class CartItemViewSet(mixins.CreateModelMixin, 
                      mixins.UpdateModelMixin, 
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


def productdetail(request):
    return render(request, 'productdetail.html')