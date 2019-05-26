from controle.models import Emprestimo, Usuario
from django.shortcuts import render, redirect
from controle.forms import PostForm


def home(request):
    return render(request, 'home.html', {'emprestimos': Emprestimo.objects.all()})


def add_user(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user_nome = form.cleaned_data['nome']
            user_telefone = form.cleaned_data['telefone']
            user_tipo = form.cleaned_data['tipo']

            new_post = Usuario(nome=user_nome, telefone=user_telefone, tipo=user_tipo)
            new_post.save()
            return redirect('painel_admin')
    elif request.method == 'GET':
        return render(request, 'adicionar_usuario.html', {'form': form})


def exibir_equipamentos(request):
    return render(request, 'listar_equipamentos.html')


def exibir_registros(request):
    return render(request, 'registros.html')


def opcoes_admin(request):
    return render(request, 'opcoes_admin.html')


def logout(request):
    return render(request, 'login.html')


def exibir_ajuda(request):
    return render(request, 'ajuda.html')


def add_equipamento(request):
    return None


def editar_item(request):
    return None


def login(request):
    return render(request, 'login.html')