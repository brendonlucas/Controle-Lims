from django.contrib import admin
from django.urls import path
from controle import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('equipamentos', views.exibir_equipamentos, name='equipamentos'),
    path('adicionar_equipamento', views.add_equipamento, name='adicionar_equipamento'),
    path('adicionar_usuario', views.add_user, name='adicionar_usuario'),
    path('registros', views.exibir_registros, name='registros'),
    path('painel_admin', views.opcoes_admin, name='painel_admin'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('ajuda', views.exibir_ajuda, name='ajuda'),
    path('editar_item', views.editar_item, name='editar_item'),
]






