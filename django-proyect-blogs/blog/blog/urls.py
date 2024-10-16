from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from blog.views import vistaindex

#si tienes una view como clase debes hace as view() siempre

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',vistaindex.as_view(),name='index'),
    path('',include('apps.post.urls')),
    path('',include('apps.user.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
'''si coloco esto me dara error 404 generico pero de error en html, actualmente me da correctamente segun el mensaje
generico de django como lo muestra el material complementario'''