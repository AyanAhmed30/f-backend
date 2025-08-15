from django.urls import path
from .views import create_checkout_session, create_paypal_payment, execute_paypal_payment, get_paypal_payment_details

# Make sure these URLs match what your frontend is calling
urlpatterns = [
    # Stripe endpoint
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    
    # PayPal endpoints - Updated to match frontend calls
    path('paypal/create-payment/', create_paypal_payment, name='create_paypal_payment'),

    path('paypal/execute-payment/', execute_paypal_payment, name='execute_paypal_payment'),
    path('paypal/payment-details/<str:payment_id>/', get_paypal_payment_details, name='paypal_payment_details'),
]