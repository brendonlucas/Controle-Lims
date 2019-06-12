from django.contrib import admin
from django.urls import path
from controle import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('painel_admin/adicionar_usuario/', views.add_user, name='adicionar_usuario'),
    path('equipamentos/<int:item_id>', views.exibir_um_equipamento, name='um_equipamento'),
    path('painel_admin/', views.opcoes_admin, name='painel_admin'),
    path('painel_admin/adicionar_equipamento/', views.add_equipamento, name='adicionar_equipamento'),
    path('painel_admin/editar_item/', views.editar_item, name='editar_item'),
    path('registros', views.exibir_registros, name='registros'),
    path('equipamentos', views.exibir_equipamentos, name='equipamentos'),
    path('logout', views.logout, name='logout'),
    # path('login', views.login, name='login'),
    path('ajuda', views.exibir_ajuda, name='ajuda'),
    path('login/',views.user_login, name='login'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
