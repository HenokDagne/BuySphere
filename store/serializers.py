from rest_framework import serializers
from .models import Category, Product, ProductVariation, Cart, CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'image', 'image_url', 'stock', 'price']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

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
    cart = CartSerializer()
    product_variation = ProductVariationSerializer()
    class Meta:
        model = CartItem
        fields = ['id','user',  'cart', 'product_variation', 'quantity']