from django.forms import ModelForm
from controle.models import *


class UserForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'telefone', 'tipo']


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'quantidade', 'tipo']

