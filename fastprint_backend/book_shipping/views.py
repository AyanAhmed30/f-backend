# book_shipping/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from book.models import BookProject
from .models import ShippingRequest, BookShippingOrder
from .serializers import (
    BookProjectWithShippingSerializer, 
    BookShippingOrderSerializer,
    ShippingRequestSerializer
)

class AdminBookShippingOrdersView(generics.ListAPIView):
    """
    Admin view - shows all book projects with their shipping info
    """
    queryset = BookProject.objects.all().order_by('-created_at')
    serializer_class = BookProjectWithShippingSerializer

@api_view(['POST'])
def create_book_shipping_order(request):
    """
    Create shipping request and link it with book project
    """
    try:
        book_project_id = request.data.get('book_project_id')
        user_address = request.data.get('user_address')
        
        if not book_project_id or not user_address:
            return Response({
                'error': 'book_project_id and user_address are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get book project
        book_project = get_object_or_404(BookProject, id=book_project_id)
        
        # Check if shipping already exists for this book project
        if BookShippingOrder.objects.filter(book_project=book_project).exists():
            return Response({
                'error': 'Shipping already exists for this book project'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create shipping request
        shipping_request = ShippingRequest.objects.create(
            user_address=user_address,
            shipping_rate=request.data.get('shipping_rate'),
            tax=request.data.get('tax'),
            response_data=request.data.get('response_data')
        )
        
        # Create book shipping order (link both)
        book_shipping_order = BookShippingOrder.objects.create(
            book_project=book_project,
            shipping_request=shipping_request
        )
        
        # Return combined data
        serializer = BookShippingOrderSerializer(book_shipping_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_book_with_shipping(request, book_project_id):
    """
    Get specific book project with its shipping info
    """
    try:
        book_project = get_object_or_404(BookProject, id=book_project_id)
        serializer = BookProjectWithShippingSerializer(book_project)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookShippingOrderDetailView(generics.RetrieveUpdateAPIView):
    """
    Admin can view and update shipping order status
    """
    queryset = BookShippingOrder.objects.all()
    serializer_class = BookShippingOrderSerializer
    lookup_field = 'order_number'