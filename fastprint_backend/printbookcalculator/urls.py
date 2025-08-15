# urls.py (in your calculator app)
from django.urls import path
from . import views

urlpatterns = [
    path('dropdowns/', views.get_dropdowns, name='get_dropdowns'),
    path('bindings/', views.get_bindings_by_trim_and_page_count, name='get_bindings'),
    path('available-options/', views.get_available_options,
         name='get_available_options'),  # NEW
    path('calculate/', views.calculate_cost, name='calculate_cost'),
    path('interior-color/<int:pk>/update/', views.update_interior_color),
    path('paper-type/<int:pk>/update/', views.update_paper_type),
    path('cover-finish/<int:pk>/update/', views.update_cover_finish),
    path('binding-type/<int:pk>/update/', views.update_binding_type),

]
