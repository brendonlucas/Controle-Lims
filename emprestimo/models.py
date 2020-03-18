from django.db import models

from controle.models import *


class TipoEstadoEmprestimo(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.CharField(max_length=255)

    # t = TipoEstadoEmprestimo(nome='Emprestado', descricao='O Emprestimo foi realizado').save()
    # t = TipoEstadoEmprestimo(nome='Devolvido', descricao='O Emprestimo foi finalizado').save()


class Emprestimo(models.Model):
    equipamento = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_emprestimo')
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_emprestimo')
    tipo = models.ForeignKey(TipoEstadoEmprestimo, on_delete=models.CASCADE, related_name='tipo_emprestimo')
    #estado = models.BooleanField(default=0)
    visualisado = models.BooleanField(default=0)
    descricao = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    data_emprestimo = models.DateField(null=False)
    data_devolucao = models.DateField(null=True)
    #mensagem_rejeitado = models.CharField(max_length=255, null=True)  # tirar
    mensagem_devolucao = models.CharField(max_length=255, null=True)
