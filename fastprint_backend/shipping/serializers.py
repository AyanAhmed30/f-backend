from rest_framework import serializers
from .models import ShippingRequest, Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class ShippingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRequest
        fields = ['id', 'user_address', 'created_at', 'shipping_rate', 'tax', 'response_data']
        read_only_fields = ['id', 'created_at',  'response_data']


class ShippingInputSerializer(serializers.Serializer):
    """
    Serializer to validate user input shipping address.
    """
    country = serializers.CharField(max_length=2)
    state = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
