from django.forms import *
from django import forms


class FormQuantidade(forms.Form):
    quantidade = forms.IntegerField(label='Quantidade', min_value=1, required=True)
    descicao = forms.CharField(label='Descição', required=True, widget=forms.Textarea)


class FromComentarioRejeitado(forms.Form):
    comentario = forms.CharField(label='Comentario', required=True, min_length=10)
