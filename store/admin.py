from django.contrib import admin
from .models import Category, Product, ProductVariation


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