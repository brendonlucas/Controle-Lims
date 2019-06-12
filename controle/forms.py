from django.forms import *
from controle.models import *
from django import forms


class UserForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'nome_de_usuario', 'email', 'senha', 'telefone', 'tipo']
        widgets = {'senha': forms.PasswordInput, 'email': forms.EmailInput, 'telefone': forms.NumberInput}


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'quantidade', 'tipo', 'imagem']


class LoginForm(forms.Form):
    username = forms.CharField(label='Nome', max_length=16)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, max_length=10)
