from usuarios.views import RegistrarUsuarioView, RegistrarUsuarioAdminView
from django.urls import path


urlpatterns = [
    path('registrar/', RegistrarUsuarioView.as_view(), name="adicionar_usuario"),
    path('registrar_administrador/', RegistrarUsuarioAdminView.as_view(), name="adicionar_admin"),
]