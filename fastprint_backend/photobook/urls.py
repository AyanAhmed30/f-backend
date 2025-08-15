from django.urls import path
from . import views

urlpatterns = [
    path('dropdowns/', views.get_dropdowns, name='photobook-dropdowns'),
    path('calculate/', views.calculate_price, name='photobook-calculate'),
    path('bindings/', views.get_bindings, name='photobook-bindings'),

    # Update Endpoints
    path('binding-type/<int:pk>/update/', views.update_binding),
    path('interior-color/<int:pk>/update/', views.update_interior_color),
    path('paper-type/<int:pk>/update/', views.update_paper_type),
    path('cover-finish/<int:pk>/update/', views.update_cover_finish),
    path('spine/<int:pk>/update/', views.update_spine),
    path('exterior-color/<int:pk>/update/', views.update_exterior_color),
    path('foil-stamping/<int:pk>/update/', views.update_foil_stamping),
    path('screen-stamping/<int:pk>/update/', views.update_screen_stamping),
]
