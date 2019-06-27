from django.forms import *
from controle.models import *
from django import forms


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'quantidade', 'tipo', 'imagem']


class LoginForm(forms.Form):
    username = forms.CharField(label='Nome', max_length=16)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, max_length=10)
