from django.forms import *
from controle.models import *
from django import forms


class ItemForm(forms.Form):
    nome = forms.CharField(required=True)
    quantidade = forms.IntegerField(required=True)
    codigo_tombamento = forms.CharField(required=False)
    imagem = forms.FileField(required=False)
    tipo = forms.CharField(required=True)


class ItemFormEdit(ModelForm):
    imagem = forms.FileField(label='Imagem', required=False)


    class Meta:
        model = Item
        fields = ['nome', 'quantidade', 'codigo_tombamento', 'tipo', 'imagem']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo_tombamento': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='Nome', max_length=16)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, max_length=10)


class FormAddUnidade(forms.Form):
    quantidade = forms.IntegerField(required=True)


class FormMudarStatus(forms.Form):
    status = forms.CharField(required=True)
