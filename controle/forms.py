from django.forms import ModelForm

from controle.models import Usuario


class PostForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'telefone', 'tipo']
