from usuarios import views
from emprestimo import views
from django.urls import path

urlpatterns = [
    path('emprestimo/<int:item_id>/solicitacao/', views.solicitar_item, name="solicitar_emprestimo"),
    path('solicitacoes/', views.exibe_solicitacoes, name="exibir_solicitacoes"),
    path('solicitacoes/<int:solicitacao_id>/aceitar/', views.aceita_solicitacao, name="aceita_solicitacao"),
    path('solicitacoes/<int:solicitacao_id>/rejeitar/', views.rejeita_solicitacao, name="rejeita_solicitacao"),
    path('solicitacoes/<int:solicitacao_id>/detalhes/', views.exibir_detalhes, name="exibir_detalhes_solicitacao"),
    path('emprestimos/<int:emprestimo_id>/devolucao/', views.fazer_devolucao_normal, name="item_devolvido"),
    path('emprestimos/<int:emprestimo_id>/devolucao-parcial/', views.fazer_devolucao_parcial, name="item_devolvido_parcial"),
    path('emprestimos/finalizados/', views.exibir_emprestimos_finalizados, name="emprestimos_finalizados"),
    path('emprestimos/', views.exibir_emprestimos, name='emprestimos'),
    path('reservar/<int:item_id>/', views.reservar_equipamento, name='reservar_equipamento'),
    path('erro', views.pag_falha, name='pag_falha'),


]
