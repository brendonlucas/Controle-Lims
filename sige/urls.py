from django.contrib import admin
from django.urls import path, include
from controle import views, urls
from django.template.response import TemplateResponse

from django.conf import settings
from django.conf.urls.static import static

handler404 = 'usuarios.views.handler404'
handler500 = 'usuarios.views.handler500'

urlpatterns = [
    path('', include(urls)),
    path('', include('usuarios.urls')),
    path('', include('emprestimo.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

