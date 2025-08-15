from django.urls import path
from . import views

urlpatterns = [
    path('dropdowns/', views.get_dropdowns),
    path('calculate/', views.calculate_price),
    path('bindings/', views.get_bindings),

    # 🆕 Update Endpoints
    path('binding-type/<int:pk>/update/', views.update_binding_type),
    path('interior-color/<int:pk>/update/', views.update_interior_color),
    path('paper-type/<int:pk>/update/', views.update_paper_type),
    path('cover-finish/<int:pk>/update/', views.update_cover_finish),
]
