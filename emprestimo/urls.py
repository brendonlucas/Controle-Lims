from usuarios import views
from emprestimo import views
from django.urls import path

urlpatterns = [
    path('emprestimo/<int:item_id>/solicitacao/', views.solicitar_item, name="solicitar_emprestimo"),
    path('solicitacoes/', views.exibe_solicitacoes, name="exibir_solicitacoes"),
    path('solicitacao/<int:solicitacao_id>/aceitar', views.aceita_solicitacao, name="aceita_solicitacao"),
    path('solicitacao/<int:solicitacao_id>/rejeitar/', views.rejeita_solicitacao, name="rejeita_solicitacao"),
    path('solicitacao/<int:solicitacao_id>/rejeitar/', views.rejeita_solicitacao, name="rejeita_solicitacao"),
    path('solicitacao/<int:solicitacao_id>/detalhes/', views.exibir_detalhes, name="exibir_detalhes_solicitacao"),
    path('emprestimos', views.exibir_emprestimos, name='emprestimos'),

]
