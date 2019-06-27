from django.contrib import admin
from django.urls import path, include
from controle import views, urls

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', include(urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
