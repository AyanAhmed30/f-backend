from django.urls import path
from . import views

urlpatterns = [
    path('dropdowns/', views.get_dropdowns),
    path('bindings/', views.get_bindings),
    path('calculate/', views.calculate_price),

    # Update endpoints
    path('interior-color/<int:pk>/update/', views.update_price('interior')),
    path('paper-type/<int:pk>/update/', views.update_price('paper')),
    path('cover-finish/<int:pk>/update/', views.update_price('cover')),
    path('binding-type/<int:pk>/update/', views.update_price('binding')),
]
