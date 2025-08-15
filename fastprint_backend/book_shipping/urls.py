# book_shipping/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Admin endpoint - shows all book projects with shipping
    path('admin-book-shipping-orders/', 
         views.AdminBookShippingOrdersView.as_view(), 
         name='admin-book-shipping-orders'),
    
    # Create shipping for a book project
    path('create-shipping-order/', 
         views.create_book_shipping_order, 
         name='create-shipping-order'),
    
    # Get specific book with shipping
    path('book-with-shipping/<int:book_project_id>/', 
         views.get_book_with_shipping, 
         name='book-with-shipping'),
    
    # Admin can update order status
    path('order/<str:order_number>/', 
         views.BookShippingOrderDetailView.as_view(), 
         name='shipping-order-detail'),
]