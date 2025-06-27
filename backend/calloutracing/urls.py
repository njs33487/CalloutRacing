"""
URL configuration for calloutracing project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="CalloutRacing API",
      default_version='v1',
      description="API for CalloutRacing application",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@calloutracing.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

def root_view(request):
    """Simple root view to show API is working"""
    return JsonResponse({
        "message": "CalloutRacing API is running!",
        "version": "1.0.0",
        "endpoints": {
            "api": "/api/",
            "admin": "/admin/",
            "docs": "/api/docs/",
            "contact": "/api/contact/",
            "health": "/health/"
        }
    })

def health_check(request):
    """Health check endpoint to verify database connection"""
    from django.db import connection
    from django.db.utils import OperationalError
    
    try:
        # Test database connection
        connection.ensure_connection()
        db_status = "connected"
    except OperationalError:
        db_status = "disconnected"
    
    return JsonResponse({
        "status": "healthy",
        "database": db_status,
        "debug": settings.DEBUG,
        "allowed_hosts": settings.ALLOWED_HOSTS
    })

urlpatterns = [
    path('', root_view, name='root'),
    path('health/', health_check, name='health'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 