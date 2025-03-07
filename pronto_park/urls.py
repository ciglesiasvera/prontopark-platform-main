from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('dashboards/', include('dashboards.urls')),
    path('parkings/', include('parkings.urls')),
    path('residences/', include('residences.urls')),
    path('reservations/', include('reservations.urls')),
    path('alerts/', include('alerts.urls')),
    path('', include('home.urls')),  # Asumiendo que tienes una app 'home' para la página principal
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)