"""
URL configuration for quiz_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
import os

def debug_static(request):
    """Debug view to check static files configuration"""
    static_root = getattr(settings, 'STATIC_ROOT', None)
    static_url = getattr(settings, 'STATIC_URL', None)
    is_vercel = getattr(settings, 'IS_VERCEL', False)
    debug = getattr(settings, 'DEBUG', False)
    
    static_files_exist = False
    admin_css_exists = False
    
    if static_root:
        static_files_exist = os.path.exists(static_root)
        admin_css_path = os.path.join(static_root, 'admin', 'css', 'base.css')
        admin_css_exists = os.path.exists(admin_css_path)
    
    return JsonResponse({
        'static_root': static_root,
        'static_url': static_url,
        'is_vercel': is_vercel,
        'debug': debug,
        'static_files_exist': static_files_exist,
        'admin_css_exists': admin_css_exists,
        'staticfiles_storage': getattr(settings, 'STATICFILES_STORAGE', None),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('quiz_api.urls')),
    path('debug-static/', debug_static, name='debug-static'),  # Debug endpoint

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve static files in development and as fallback in production
if settings.DEBUG or settings.IS_VERCEL:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
