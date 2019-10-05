from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as v
from usuarios.views import RegistrarUsuarioView, RegistrarUsuarioAdminView
from . import views
from emprestimo.views import exibir_emprestimos
from .views import Editar


urlpatterns = [
    path('', exibir_emprestimos, name='root'),
    path('equipamentos', views.exibir_equipamentos, name='equipamentos'),
    path('equipamento/novo/', views.add_equipamento, name='adicionar_equipamento'),
    path('equipamento/<int:item_id>', views.exibir_um_equipamento, name='equipamento'),
    # path('equipamento/<pk>/editar/', Editar.as_view(), name='editar_equipamento'),
    path('equipamento/<pk>/editar/', views.item_editar, name='editar_equipamento'),
    path('equipamento/<int:item_id>/excluir/',views.excluir_item, name='excluir'),
    path('excluidos',views.exibe_excluidos, name='itens_excluidos'),
    path('painel_administração/', views.opcoes_admin, name='painel_admin'),
    path('registrar/', RegistrarUsuarioView.as_view(), name="adicionar_usuario"),
    path('registrar_administrador/', RegistrarUsuarioAdminView.as_view(), name="adicionar_admin"),
    path('login/', v.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', v.LogoutView.as_view(template_name='login.html'), name="logout"),

]
