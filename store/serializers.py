from rest_framework import serializers
from .models import Category, Product, ProductVariation, Cart, CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    def update(self, instance, validated_data):
        Category_data = validated_data.pop('category', None)
        if Category_data:
            CategorySerializer = self.fields['category']
            Category_instance = instance.category
            Category = CategorySerializer.update(Category_instance, Category_data)

        return super().update(instance, validated_data)
   
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'image', 'stock', 'price'] 

class ProductVariationSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ProductVariation
        fields = ['id', 'product', 'color', 'image', 'additional_price', 'stock']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    product_variation = ProductVariationSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product_variation', 'quantity']