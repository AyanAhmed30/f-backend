from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),

    path('api/pricing/', include('pricing.urls')),
    path('api/calculator/', include('printbookcalculator.urls')),
    path('api/comicbook/', include('comicbook.urls')),


    path('api/photobook/', include('photobook.urls')),
    path('api/magazine/', include('magazine.urls')),
    path('api/yearbook/', include('yearbook.urls')),
    path('api/calender/', include('calender.urls')),
    path('api/', include('shipping.urls')),
    path('api/book/', include('book.urls')),
    path('api/', include('payment.urls')),
    path('api/book-shipping/', include('book_shipping.urls')),








]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
