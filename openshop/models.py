from django.db import models
import uuid

# Create your models here.
class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    description = models.TextField()
    shop = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    picture = models.CharField(max_length=255)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)