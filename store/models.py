from django.db import models
from django.contrib.auth.models import User

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
class CreateProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True)  
class Address(models.Model):
    customer = models.ForeignKey(CreateProfile, related_name='addresses', on_delete=models.CASCADE) 
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.zip_code}, {self.country}"



class Cart(models.Model):
    user = models.OneToOneField(CreateProfile, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.user.username} - {self.created_at}"    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    productVariation = models.ForeignKey(ProductVariation, related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)        

    class Meta:
        unique_together = ('cart', 'productVariation') # Ensure each product_variation appears only once per cart

    def __str__(self):
        return f"{self.productVariation .name} -{self.productVariation.color}- {self.quantity}"

    @property
    def get_total(self):
        return self.productVariation.additional_price * self.quantity


class Order(models.Model):
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    customer = models.ForeignKey(CreateProfile, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    

    def __str__(self):
        return f"{self.customer.user.username} - {self.total_price} "
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    productVariation = models.ForeignKey(ProductVariation, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'productVariation')  # Ensure each product_variation appears only once per order

    def __str__(self):
        return f"{self.productVariation.product.name} - {self.productVariation.color} - {self.quantity}"

    @property
    def get_total(self):
        return self.productVariation.additional_price * self.quantity


class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(CreateProfile, on_delete=models.CASCADE)
    street = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=250)
    full_address = models.TextField(null=True, blank=True)



    def __str__(self):
        return f'{self.street}, {self.city}, {self.zip_code}'

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Credit Card', 'Credit Card'),
        ('PayPal', 'PayPal'),
        ('Google Pay', 'Google Pay'),
        ('COD', 'Cash on Delivery'),
    ]
    #order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')  # One payment per order
    transaction_id = models.CharField(max_length=255, blank=True, null=True) # From payment gateway
    customer = models.ForeignKey(CreateProfile, related_name='payment_methods', on_delete=models.CASCADE)    
    method = models.CharField(max_length=25, choices=PAYMENT_METHODS, default='paypal')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.customer.user.username} - {self.method} - {self.amount} - {self.status}"     