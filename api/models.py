import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    This allows for additional fields or methods in the future.
    """
    # You can add additional fields here if needed
    pass

class Product(models.Model):
    """
    Model representing a product in the e-commerce platform.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    @property
    def in_stock(self):
        """
        Returns True if the product is in stock, otherwise False.
        """
        return self.stock > 0

    def __str__(self):
        return self.name
    
class Order(models.Model):
    """
    Model representing an order in the e-commerce platform.
    """
    class Status(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'
            
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
        
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
        
        
    def __str__(self):
        return f"Order {self.order_id} by {self.user.username} - {self.status}"
  
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)   
            
    @property
    def item_subtotal(self):
        """
        Returns the subtotal for this order item (quantity * product price).
        """
        return self.quantity * self.product.price   
            
    def __str__(self) -> str:
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"
            
            