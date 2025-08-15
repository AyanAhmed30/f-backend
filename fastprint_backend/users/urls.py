from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    VerifyEmailView,
    PasswordResetRequestView,
    PasswordResetView,
    AdminUserListView,
    AdminUserDeleteView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('request-reset-password/', PasswordResetRequestView.as_view(), name='request-reset-password'),
    path('reset-password/<uidb64>/<token>/', PasswordResetView.as_view(), name='reset-password'),

    # Admin user management URLs
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:user_id>/delete/', AdminUserDeleteView.as_view(), name='admin-user-delete'),
]
