from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import *
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password, check_password

from controle.models import *
from emprestimo.models import *
from usuarios.forms import *


def get_usuario_logado(request):
    return request.user


@method_decorator(login_required, name='dispatch')
class RegistrarUsuarioView(View):
    template_name = 'adicionar_usuario.html'

    def get(self, request):
        if get_usuario_logado(request).is_superuser:
            return render(request, self.template_name, {'user_logado': get_usuario_logado(request)})

        else:
            return render(request, 'emprestimos.html', {'emprestimos': Emprestimo.objects.all().order_by('data_emprestimo'),
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


@method_decorator(login_required, name='dispatch')
class RegistrarUsuarioAdminView(View):
    template_name = 'adicionar_usuario.html'

    def get(self, request):
        return render(request, self.template_name, {'user_logado': get_usuario_logado(request)})



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


@login_required
def exibir_usuarios(request):
    return render(request, 'exibir_usuarios.html',
                  {'user_logado': get_usuario_logado(request), 'usuarios': Usuario.objects.all()})


@login_required
def exibir_um_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    emprestimo = Emprestimo.objects.filter(solicitante=usuario_id).filter(tipo=2)
    return render(request, 'exibir.html', {'emprestimos': emprestimo, 'usuario': usuario,
                                           'user_logado': get_usuario_logado(request)})


@login_required
def exibir_perfil(request):
    user_profile = Usuario.objects.get(user=get_usuario_logado(request).id)
    emprestimo = Emprestimo.objects.filter(solicitante=user_profile.id)
    return render(request, 'my_profile.html',
                  {'emprestimos': emprestimo, 'user_logado': get_usuario_logado(request), 'user_profile': user_profile})


@method_decorator(login_required, name='dispatch')
class TrocarSenhaUserView(View):
    template_name = 'alterar_senha.html'

    def get(self, request):
        return render(request, self.template_name, {'user_logado': get_usuario_logado(request)})

    def post(self, request):
        form = TrocarSenhaUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.data
            nova_senha = dados_form['new_pass']
            senha_atual = dados_form['current_pass']
            if get_usuario_logado(request).check_password(senha_atual):
                hashed_pwd = make_password(nova_senha)
                user = get_usuario_logado(request)
                user.password = hashed_pwd
                user.save()

            return redirect('exibe_meu_perfil', get_usuario_logado(request).id)
        return render(request, self.template_name, {'form': form, 'user_logado': get_usuario_logado(request)})

