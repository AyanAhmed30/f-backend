# book_shipping/models.py

from django.db import models
from book.models import BookProject

class Warehouse(models.Model):
    """
    Warehouse (origin) address stored by admin.
    """
    name = models.CharField(max_length=255, default="Main Warehouse")
    country_alpha2 = models.CharField(max_length=2)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    address_line = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.city})"


class ShippingRequest(models.Model):
    """
    Stores user destination address and Easyship response.
    """
    user_address = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_rate = models.FloatField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        city = self.user_address.get("city", "Unknown")
        country = self.user_address.get("country", "Unknown")
        return f"Shipping request to {city}, {country} at {self.created_at:%Y-%m-%d %H:%M}"


class BookShippingOrder(models.Model):
    """
    Links BookProject with ShippingRequest - Main model for admin
    """
    book_project = models.OneToOneField(
        BookProject, 
        on_delete=models.CASCADE, 
        related_name='book_shipping_order'
    )
    shipping_request = models.OneToOneField(
        ShippingRequest, 
        on_delete=models.CASCADE, 
        related_name='book_order'
    )
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=50, 
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate unique order number
            import uuid
            self.order_number = f"BSO-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.book_project.title}"

    class Meta:
        verbose_name = "Book Shipping Order"
        verbose_name_plural = "Book Shipping Orders"