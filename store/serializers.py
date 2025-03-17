from rest_framework import serializers
from .models import Category, Product, ProductVariation, Cart, CartItem, Order, OrderItem, ShippingAddress

class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)    

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
    cartitems_detail = CartItemSerializer(source='items', many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user','cartitems_detail', 'total_price']

    def get_total_price(self, obj):
        total = sum(item.productVariation.additional_price + item.productVariation.product.price * item.quantity for item in obj.items.all())
        return total
    
class OrderItemSerailizer(serializers.ModelSerializer):
    productVariation = ProductVariationSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['id','productVariation','quantity']


class OrderSerializer(serializers.ModelSerializer):
    orders = OrderItemSerailizer(source='items', many=True, read_only=True)
    class Meta:
        model = Order  
        fields = ['id', 'customer', 'orders', 'created_at', 'total_price', 'status' ]

        def __str__(self):
            return f"{self.customer.user.username} - {self.total_price} "

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id', 'order', 'customer', 'street', 'city', 'zip_code', 'full_address']
                






