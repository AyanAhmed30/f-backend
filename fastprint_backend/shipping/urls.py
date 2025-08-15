from django.urls import path
from .views import ShippingRateAPIView, ShippingRequestListAPIView, WarehouseListAPIView
from .views import ShippingRateAPIView, SaveShippingAPIView


urlpatterns = [
    path('shipping-rate/', ShippingRateAPIView.as_view(), name='shipping-rate'),
        path('save-shipping/', SaveShippingAPIView.as_view(), name='save-shipping'),
        path('shipping-requests/', ShippingRequestListAPIView.as_view(), name='shipping-request-list'),
            path('warehouses/', WarehouseListAPIView.as_view(), name='warehouse-list'),

        

]
