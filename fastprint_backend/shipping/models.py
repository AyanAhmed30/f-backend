from django.db import models


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
