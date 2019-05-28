from django.db import models


class TipoEquipamento(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Item(models.Model):
    nome = models.CharField(max_length=50)
    quantidade = models.IntegerField()
    tipo = models.ForeignKey(TipoEquipamento, on_delete=models.CASCADE)


class TipoUsuario(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)


class Emprestimo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField(null=True)


