from django.urls import path
from . import views

urlpatterns = [
    path('dropdowns/', views.get_comic_dropdowns),
    path('bindings/', views.get_comic_bindings),
    path('calculate/', views.calculate_comic_cost),
    
    
    
    # NEW update routes
    path('binding-type/<int:pk>/update/', views.update_comic_binding_type),
    path('interior-color/<int:pk>/update/', views.update_comic_interior_color),
    path('paper-type/<int:pk>/update/', views.update_comic_paper_type),
    path('cover-finish/<int:pk>/update/', views.update_comic_cover_finish),
    path('comic/all-bindings/', views.get_all_comic_bindings),

]