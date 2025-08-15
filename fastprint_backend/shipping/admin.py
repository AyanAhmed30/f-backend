from django.contrib import admin
from .models import Warehouse  # apne model ka correct path

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country_alpha2', 'postal_code')
    search_fields = ('name', 'city', 'country_alpha2')
