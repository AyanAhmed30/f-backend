from django.urls import path
from .views import admin_all_orders

from .views import (
    UploadBookProjectView,
    user_books,
    book_detail,
    update_book,
    delete_book,
)

urlpatterns = [
    path('upload-book/', UploadBookProjectView.as_view(), name='upload-book'),
    path('my-books/', user_books, name='my-books'),
    path('books/<int:pk>/', book_detail, name='book-detail'),          # GET single project
    path('books/<int:pk>/update/', update_book, name='book-update'),   # PUT/PATCH update project
    path('<int:pk>/delete/', delete_book, name='book-delete'),
    path("all-orders/", admin_all_orders, name="admin-all-orders"),
]
