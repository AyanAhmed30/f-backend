# book_shipping/serializers.py

from rest_framework import serializers
from book.models import BookProject
from .models import ShippingRequest, BookShippingOrder

class ShippingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRequest
        fields = [
            'id', 'user_address', 'shipping_rate', 
            'tax', 'created_at', 'response_data'
        ]

class BookProjectWithShippingSerializer(serializers.ModelSerializer):
    shipping = serializers.SerializerMethodField()
    
    class Meta:
        model = BookProject
        fields = [
            'id', 'title', 'language', 'category', 'page_count',
            'created_at', 'binding_type', 'cover_finish', 'interior_color',
            'paper_type', 'trim_size', 'pdf_file', 'cover_file',
            'cover_description', 'shipping'
        ]

    def get_shipping(self, obj):
        try:
            # Get shipping data through BookShippingOrder
            book_shipping_order = BookShippingOrder.objects.get(book_project=obj)
            shipping_request = book_shipping_order.shipping_request
            
            return {
                'order_number': book_shipping_order.order_number,
                'status': book_shipping_order.status,
                'shipping_rate': shipping_request.shipping_rate,
                'tax': shipping_request.tax,
                'user_address': shipping_request.user_address,
                'created_at': shipping_request.created_at,
                'response_data': shipping_request.response_data
            }
        except BookShippingOrder.DoesNotExist:
            return None

class BookShippingOrderSerializer(serializers.ModelSerializer):
    book_project = BookProjectWithShippingSerializer(read_only=True)
    shipping_request = ShippingRequestSerializer(read_only=True)
    
    class Meta:
        model = BookShippingOrder
        fields = [
            'id', 'order_number', 'status', 'created_at', 
            'updated_at', 'book_project', 'shipping_request'
        ]