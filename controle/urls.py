from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

from .views import Editar

urlpatterns = [
    path('', views.opcoes_admin, name='root'),
    path('equipamentos', views.exibir_equipamentos, name='equipamentos'),
    path('equipamento/novo', views.add_equipamento, name='adicionar_equipamento'),
    path('equipamento/<int:item_id>', views.exibir_um_equipamento, name='equipamento'),
    path('equipamento/<pk>/editar/', Editar.as_view(), name='editar_equipamento'),
    path('editar_item/', views.editar_item, name='editar_item'),
    path('emprestimos', views.exibir_emprestimos, name='emprestimos'),
    path('adicionar_usuario/', views.add_user, name='adicionar_usuario'),
]
