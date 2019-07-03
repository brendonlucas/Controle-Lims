from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import *
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth.decorators import permission_required

from controle.models import *
from usuarios.forms import RegistrarUsuarioForm


def get_usuario_logado(request):
    return request.user


# @method_decorator(login_required, name='dispatch')
class RegistrarUsuarioView(View):
    template_name = 'adicionar_usuario.html'

    def get(self, request):
        if get_usuario_logado(request).is_superuser:
            return render(request, self.template_name, {'user_logado': get_usuario_logado(request)})

        else:
            return render(request, 'emprestimos.html', {'emprestimos': Emprestimo.objects.all(),
                                                        'user_logado': get_usuario_logado(request)})

    def post(self, request):
        if get_usuario_logado(request).is_superuser:
            form = RegistrarUsuarioForm(request.POST)
            if form.is_valid():
                dados_form = form.cleaned_data
                usuario = User.objects.create_user(username=dados_form['nome'], email=dados_form['email'],
                                                   password=dados_form['senha'], first_name=dados_form['first_name'],
                                                   last_name=dados_form['last_name'])

                tipo = TipoUsuario.objects.get(id=1)
                usuario_dados = Usuario(telefone=dados_form['telefone'], user=usuario, tipo=tipo)

                usuario_dados.save()
                return redirect('root')
            return render(request, self.template_name, {'form': form, 'user_logado': get_usuario_logado(request)})


# @method_decorator(login_required, name='dispatch')
class RegistrarUsuarioAdminView(View):
    template_name = 'adicionar_usuario.html'

    def get(self, request):
        if get_usuario_logado(request).is_superuser:
            return render(request, self.template_name, {'user_logado': get_usuario_logado(request)})

        else:
            return render(request, 'emprestimos.html', {'emprestimos': Emprestimo.objects.all(),
                                                        'user_logado': get_usuario_logado(request)})

    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username=dados_form['nome'], email=dados_form['email'],
                                               password=dados_form['senha'], is_superuser=True,
                                               first_name=dados_form['first_name'],
                                               last_name=dados_form['last_name'], )

            tipo = TipoUsuario.objects.get(id=2)
            usuario_dados = Usuario(telefone=dados_form['telefone'], user=usuario, tipo=tipo)

            usuario_dados.save()
            return redirect('root')

        return render(request, self.template_name, {'form': form})


def exibir_usuarios(request):
    return render(request, 'exibir_usuarios.html',
                  {'user_logado': get_usuario_logado(request), 'usuarios': Usuario.objects.all()})


def exibir_um_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    return render(request, 'exibir.html', {'usuario': usuario, 'user_logado': get_usuario_logado(request)})
