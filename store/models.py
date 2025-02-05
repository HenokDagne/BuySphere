from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='images/')

    class Meta:
        ordering = ["name"]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    class Meta:
        ordering = ["name"]

    def is_in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)  # Add a field for color
    image = models.ImageField(upload_to='images/')
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField(default=0)  # Add a stock field for each variation

    class Meta:
        unique_together = ('product', 'color')  # Ensure each product-color combination is unique

    def __str__(self):
        return f"{self.product.name} - {self.color}s"

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, unique=True)

    class Meta:
        ordering = ["-created_at"]

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    productVariation = models.ForeignKey(ProductVariation, related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)        

    class Meta:
        unique_together = ('cart', 'productVariation') # Ensure each product_variation appears only once per cart

    def __str__(self):
        return f"{self.productVariation .name} -{self.productVariation.color}- {self.quantity}"
    
    