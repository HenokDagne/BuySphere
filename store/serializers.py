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
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariation
        fields = ['id', 'product', 'color', 'image', 'image_url', 'additional_price', 'stock']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
       

        


class CartItemSerializer(serializers.ModelSerializer):
    productVariation = ProductVariationSerializer()
   

    class Meta:
        model = CartItem
        fields = ['id','cart', 'productVariation', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user','items', 'total_price']

    def get_total_price(self, obj):
        total = sum(item.productVariation.additional_price * item.quantity for item in obj.items.all())
        return total

