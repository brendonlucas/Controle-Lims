from usuarios import views
from usuarios.views import *
from django.urls import path

urlpatterns = [
    path('registrar/', RegistrarUsuarioView.as_view(), name="adicionar_usuario"),
    path('registrar_administrador/', RegistrarUsuarioAdminView.as_view(), name="adicionar_admin"),
    path('usuarios/', views.exibir_usuarios, name="exibir_usuarios"),
    path('usuario/<int:usuario_id>', views.exibir_um_usuario, name='exibe_um_usuario'),
    path('meu-perfil/<int:usuario_id>', views.exibir_perfil, name='exibe_meu_perfil'),
    path('meu-perfil/mudar_senha/', TrocarSenhaUserView.as_view(), name='mudar_senha'),
]
