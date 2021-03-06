from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import *
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password, check_password

from django.template import RequestContext

from controle.models import *
from emprestimo.models import *
from usuarios.forms import *


def get_usuario_logado(request):
    return request.user


def get_qtd_notificacoes():
    return Emprestimo.objects.filter(visualisado=0).count()


@method_decorator(login_required, name='dispatch')
class RegistrarUsuarioView(View):
    template_name = 'add_usuario.html'

    def get(self, request):
        if get_usuario_logado(request).is_superuser:
            return render(request, self.template_name, {'user_logado': get_usuario_logado(request),
                                                        'qtd_notificacoes': get_qtd_notificacoes()})
        else:
            messages.error(request, 'Acesso negado!')
            return render(request, 'pag_falha.html',
                          {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})

    def post(self, request):
        if get_usuario_logado(request).is_superuser:
            form = RegistrarUsuarioForm(request.POST)
            if form.is_valid():
                dados_form = form.cleaned_data
                usuario = User.objects.create_user(username=dados_form['nome'], email=dados_form['email'],
                                                   password=dados_form['senha'],
                                                   first_name=dados_form['first_name'],
                                                   last_name=dados_form['last_name'])
                tipo = TipoUsuario.objects.get(id=1)
                usuario_dados = Usuario(telefone=dados_form['telefone'], user=usuario, tipo=tipo)
                usuario_dados.save()
                return redirect('root')

            return render(request, self.template_name, {'form': form, 'user_logado': get_usuario_logado(request),
                                                        'qtd_notificacoes': get_qtd_notificacoes()})


@method_decorator(login_required, name='dispatch')
class RegistrarUsuarioAdminView(View):
    template_name = 'add_usuario.html'

    def get(self, request):
        if get_usuario_logado(request).is_superuser:
            return render(request, self.template_name, {'user_logado': get_usuario_logado(request),
                                                        'qtd_notificacoes': get_qtd_notificacoes()})
        else:
            messages.error(request, 'Acesso negado!')
            return render(request, 'pag_falha.html',
                          {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})

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
        return render(request, self.template_name, {'form': form,
                                                    'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def exibir_usuarios(request):
    if get_usuario_logado(request).is_superuser:
        usuarios = Usuario.objects.all().order_by('-user__first_name')
        paginator = Paginator(usuarios, 8)
        page = request.GET.get('page')
        usuarios = paginator.get_page(page)
        return render(request, 'exibir_usuarios.html',
                      {'user_logado': get_usuario_logado(request), 'usuarios': usuarios,
                       'qtd_notificacoes': get_qtd_notificacoes()})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html',
                      {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def exibir_um_usuario(request, usuario_id):
    try:
        usuario = Item.objects.get(id=usuario_id)
    except Item.DoesNotExist:
        messages.error(request, 'Usuario não encontrado!')
        return render(request, 'pag_falha.html',
                      {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})

    usuario = Usuario.objects.get(id=usuario_id)
    emprestimos = Emprestimo.objects.filter(solicitante=usuario_id).exclude(tipo=1).order_by('-data_emprestimo')
    paginator = Paginator(emprestimos, 8)
    page = request.GET.get('page')
    emprestimos = paginator.get_page(page)
    return render(request, 'exibir.html', {'emprestimos': emprestimos, 'usuario': usuario,
                                           'user_logado': get_usuario_logado(request),
                                           'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def exibir_perfil(request):
    user_profile = Usuario.objects.get(user=get_usuario_logado(request).id)
    emprestimo = Emprestimo.objects.filter(solicitante=user_profile.id)
    return render(request, 'my_profile.html', {'emprestimos': emprestimo, 'user_logado': get_usuario_logado(request),
                                               'user_profile': user_profile,
                                               'qtd_notificacoes': get_qtd_notificacoes()})


@method_decorator(login_required, name='dispatch')
class TrocarSenhaUserView(View):
    template_name = 'alterar_senha.html'

    def get(self, request):
        return render(request, self.template_name, {'user_logado': get_usuario_logado(request),
                                                    'qtd_notificacoes': get_qtd_notificacoes()})

    def post(self, request):
        form = TrocarSenhaUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.data
            nova_senha = dados_form['new_pass']
            senha_atual = dados_form['current_pass']
            name_user = dados_form['your_user']
            if name_user == get_usuario_logado(request).username:
                if get_usuario_logado(request).check_password(senha_atual):
                    hashed_pwd = make_password(nova_senha)
                    user = get_usuario_logado(request)
                    user.password = hashed_pwd
                    user.save()
                    return redirect('exibe_meu_perfil')
                else:
                    messages.error(request, 'Senha atual incorreta!')
                    redirect('mudar_senha')
            else:
                messages.error(request, 'Username incorreto!')
                redirect('mudar_senha')
        return render(request, self.template_name, {'form': form, 'user_logado': get_usuario_logado(request),
                                                    'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def exibir_ajuda(request):
    return render(request, 'pag_ajuda.html', {'user_logado': get_usuario_logado(request),
                                              'qtd_notificacoes': get_qtd_notificacoes()})


def handler404(request, exception, template_name="page_404.html"):
    response = render("page_404.html")
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render("page_404.html")
    response.status_code = 500
    return response
