from django.contrib import admin
from .models import Category, Product, ProductVariation, CreateProfile, Order, OrderItem, ShippingAddress


@admin.register(Category)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'image']
    search_fields = ['name', 'slug']
    list_editable = ['name', 'slug', 'image']
    list_filter = ['name']
@admin.register(Product)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'category', 'image', 'stock']
    search_fields = ['name']
    list_editable = ['name', 'description', 'price', 'category', 'image', 'stock']
    list_filter = ['name', 'price']
    
    
@admin.register(ProductVariation)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'color', 'image', 'additional_price', 'stock']
    search_fields = ['product__name', 'color']
    list_editable = ['product', 'color', 'image', 'additional_price', 'stock']
    list_filter = ['product__name', 'color']

@admin.register(CreateProfile)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user__email', 'first_name', 'last_name', 'phone']
    list_editable = ['user', 'first_name', 'last_name', 'phone']
    search_fields = ['user_email', 'first_name', 'last_name']
    list_filter = ['user__email', 'first_name', 'last_name']

@admin.register(Order)
class AuthorAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'customer', 'created_at', 'total_price', 'status']
    list_editable = ['customer', 'total_price', 'status', 'status']
    search_fields = [' customer.first_name', 'last_name']
    list_filter = ['created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'productVariation', 'quantity', 'product_name', 'orderId']
    list_editable = ['order', 'productVariation', 'quantity']
    search_fields = ['order', 'productVariation__product__name']
    list_filter = ['order', 'productVariation__product__name']

    def product_name(self, obj):
        return obj.productVariation.product.name
    product_name.short_description = 'Product Name'

    def orderId(self, obj):
        return obj.order.id
    orderId.short_description = 'Order ID'

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'customer', 'street', 'city', 'zip_code', 'full_address']
    list_editable = ['order', 'customer', 'street', 'city', 'zip_code', 'full_address']
    search_fields = [ 'zip_code', 'full_address']    
    list_filter = ['order', 'customer', 'street']