from rest_framework import viewsets
from django.shortcuts import render
from .models import Category, Product, ProductVariation
from .serializers import CategorySerializer, ProductSerializer, ProductVariationSerializer
def home(request):
    return render(request, 'index.html')
 
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductVariationViewSet(viewsets.ModelViewSet):
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationSerializer
        




