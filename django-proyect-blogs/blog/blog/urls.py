from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from blog.views import vistaindex, not_found_view, internal_error_view, forbidden_view

#si tienes una view como clase debes hace as view() siempre

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',vistaindex.as_view(),name='index'),
    path('',include('apps.post.urls')),
    path('',include('apps.user.urls')),
]

# Manejadores de errores
handler404 = not_found_view
handler500 = internal_error_view
handler403 = forbidden_view

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
