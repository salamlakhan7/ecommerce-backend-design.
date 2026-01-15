"""
URL configuration for ecommerce_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ecommerce.views import api_root

urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/', include('ecommerce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
