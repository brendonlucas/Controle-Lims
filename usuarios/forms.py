from django import forms
from django.contrib.auth.models import User


class RegistrarUsuarioForm(forms.Form):
    nome = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(required=True)
    telefone = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        if not super(RegistrarUsuarioForm, self).is_valid():
            self.adiciona_erro('Por favor, verifique os dados informados')
            valid = False

        user_exists = User.objects.filter(username=self.cleaned_data['nome']).exists()
        if user_exists:
            self.adiciona_erro('Usuário já existente.')
            valid = False
        return valid

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(message)


class TrocarSenhaUsuarioForm(forms.Form):
    your_user = forms.CharField(required=True)
    current_pass = forms.CharField(required=True)
    new_pass = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        user_exists = User.objects.filter(username=self.data['your_user']).exists()

        print(user_exists)
        if not user_exists:
            self.adiciona_erro('Usuário invalido.')
            valid = False
        elif user_exists:
            user = User.objects.get(username=self.data['your_user'])
            senha_atual = self.data['current_pass']
            if not user.check_password(senha_atual):
                print("tt")
                self.adiciona_erro('A senha informada não confere!')
                valid = False

        return valid

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(message)

