from django.urls import path
from .views import (
    DropdownOptionsView,
    PricingCalculationView,
    BindingTypeUpdateView,
    SpineTypeUpdateView,
    ExteriorColorUpdateView,
    FoilStampingUpdateView,
    ScreenStampingUpdateView,
    CornerProtectorUpdateView,
    InteriorColorUpdateView,
    PaperTypeUpdateView
)

urlpatterns = [
    path('options/', DropdownOptionsView.as_view(), name='pricing-options'),
    path('calculate/', PricingCalculationView.as_view(), name='pricing-calculate'),

    # Update endpoints for ThesisEditSettings.jsx
    path('binding-type/<int:pk>/update/', BindingTypeUpdateView.as_view(), name='binding-type-update'),
    path('spine-type/<int:pk>/update/', SpineTypeUpdateView.as_view(), name='spine-type-update'),
    path('exterior-color/<int:pk>/update/', ExteriorColorUpdateView.as_view(), name='exterior-color-update'),
    path('foil-stamping/<int:pk>/update/', FoilStampingUpdateView.as_view(), name='foil-stamping-update'),
    path('screen-stamping/<int:pk>/update/', ScreenStampingUpdateView.as_view(), name='screen-stamping-update'),
    path('corner-protector/<int:pk>/update/', CornerProtectorUpdateView.as_view(), name='corner-protector-update'),
    path('interior-color/<int:pk>/update/', InteriorColorUpdateView.as_view(), name='interior-color-update'),
    path('paper-type/<int:pk>/update/', PaperTypeUpdateView.as_view(), name='paper-type-update'),
]
