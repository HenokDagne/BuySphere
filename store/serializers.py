from rest_framework import serializers
from .models import Category, Product, ProductVariation, Cart, CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
   
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'image', 'stock', 'price'] 

class ProductVariationSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ProductVariation
        fields = ['id', 'color', 'image', 'additional_price', 'stock']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        field = ['id', 'created_at']

class CartItem(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    ProductVariation = ProductVariationSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'productVariation', 'quantity']


