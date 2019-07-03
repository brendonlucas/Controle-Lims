from usuarios import views
from usuarios.views import RegistrarUsuarioView, RegistrarUsuarioAdminView
from django.urls import path


urlpatterns = [
    path('registrar/', RegistrarUsuarioView.as_view(), name="adicionar_usuario"),
    path('registrar_administrador/', RegistrarUsuarioAdminView.as_view(), name="adicionar_admin"),
    path('usuarios/', views.exibir_usuarios, name="exibir_usuarios"),
    path('usuario/<int:usuario_id>', views.exibir_um_usuario, name='exibe_um_usuario'),
]