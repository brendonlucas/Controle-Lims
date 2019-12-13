from django.urls import path
from django.contrib.auth import views as v
from usuarios.views import RegistrarUsuarioView, RegistrarUsuarioAdminView
from . import views
from emprestimo.views import exibir_emprestimos

urlpatterns = [
    path('', exibir_emprestimos, name='root'),
    path('equipamento/', views.exibir_equipamentos, name='equipamentos'),
    path('equipamento/novo/', views.add_equipamento, name='adicionar_equipamento'),
    path('equipamento/<int:item_id>/', views.exibir_um_equipamento, name='equipamento'),
    path('equipamento/<pk>/editar/', views.item_editar, name='editar_equipamento'),
    path('equipamento/<int:item_id>/excluir/', views.excluir_item, name='excluir'),
    path('equipamento/<int:item_id>/Restaurar/', views.restaurar_item, name='restaurar_item'),
    path('equipamento/excluidos/', views.exibe_excluidos, name='itens_excluidos'),
    path('painel_administracao/', views.opcoes_admin, name='painel_admin'),
    path('registrar/', RegistrarUsuarioView.as_view(), name="adicionar_usuario"),
    path('registrar_administrador/', RegistrarUsuarioAdminView.as_view(), name="adicionar_admin"),
    path('login/', v.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', v.LogoutView.as_view(template_name='login.html'), name="logout"),

]
