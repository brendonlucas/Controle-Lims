from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from controle import views, urls
from django.template.response import TemplateResponse

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

handler404 = 'usuarios.views.handler404'
handler500 = 'usuarios.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls)),
    path('', include('usuarios.urls')),
    path('', include('emprestimo.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]



