from django.contrib.auth.models import User
from django.db import models


class TipoEquipamento(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Item(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    quantidade_emprestada = models.IntegerField(default=0)
    quantidade_descartada = models.IntegerField(default=0)
    codigo_tombamento = models.CharField(max_length=100, null=True, default=None)
    tipo = models.ForeignKey(TipoEquipamento, on_delete=models.CASCADE)
    imagem = models.FileField(upload_to='documents/%Y/%m/%d', default='documents/1111/sem_foto.jpg')
    excluido = models.BooleanField(default=False)
    em_operacao = models.BooleanField(default=1, null=True)


class TipoUsuario(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
    telefone = models.IntegerField()
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    @property
    def email(self):
        return self.user.email

# from emprestimo.models import *
# from controle.models import *

# t = TipoUsuario(nome='Normal', descricao='Usuario com acesso limitado').save()
# t = TipoUsuario(nome='Administrador', descricao='Usuario com acesso total ao sistema').save()

# TipoEquipamento(nome='Consumivel', descricao='Item do tipo consumivel que pode sofrer perda').save()
# TipoEquipamento(nome='Permanente', descricao='Item do tipo Permanente que caso haja perda, medidas serão tomadas').save()

# t = TipoEstadoEmprestimo(nome='Solicitacao', descricao='Pedido no estado de solicitação').save()
# t = TipoEstadoEmprestimo(nome='Aceito', descricao='Pedido foi aceito').save()
# t = TipoEstadoEmprestimo(nome='Rejeitado', descricao='Pedido está rejeitado').save()
# t = TipoEstadoEmprestimo(nome='Finalizado', descricao='Emprestimo está finalizado').save()

# t = TipoEstadoEmprestimo(nome='Emprestado', descricao='O Emprestimo foi realizado').save()
# t = TipoEstadoEmprestimo(nome='Devolvido', descricao='O Emprestimo foi finalizado').save()