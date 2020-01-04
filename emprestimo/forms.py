from django.forms import *
from django import forms


class FormQuantidade(forms.Form):
    quantidade = forms.IntegerField(label='Quantidade', min_value=1, required=True)
    descricao = forms.CharField(label='Descrição', required=True, widget=forms.Textarea)


class FormQuantidadeDevolucao(forms.Form):
    quantidade = forms.IntegerField(label='Quantidade', min_value=1, required=True)
    quantidade_defeituoso = forms.IntegerField(label='Quantidade Defeituoso', min_value=1, required=True)
    descricao = forms.CharField(label='Descrição', required=True, widget=forms.Textarea)



class FromComentarioRejeitado(forms.Form):
    comentario = forms.CharField(label='Comentario', required=True, min_length=10)
