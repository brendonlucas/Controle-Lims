from controle.models import *
from django.shortcuts import render, redirect
from controle.forms import *


def home(request):
    return render(request, 'home.html', {'emprestimos': Emprestimo.objects.all()})


def add_user(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_nome = form.cleaned_data['nome']
            user_telefone = form.cleaned_data['telefone']
            user_tipo = form.cleaned_data['tipo']
            new_post = Usuario(nome=user_nome, telefone=user_telefone, tipo=user_tipo)
            new_post.save()
            return redirect('painel_admin')

    elif request.method == 'GET':
        return render(request, 'adicionar_usuario.html', {'form': form})


def add_equipamento(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            qtd = form.cleaned_data['quantidade']
            tipo = form.cleaned_data['tipo']
            new = Item(nome=nome, quantidade=qtd, tipo=tipo)
            new.save()
            return redirect('equipamentos')

    elif request.method == 'GET':
        return render(request, 'adicionar_equipamento.html', {'form': form})


def exibir_equipamentos(request):
    return render(request, 'listar_equipamentos.html', {'itens': Item.objects.all()})


def exibir_registros(request):
    return render(request, 'registros.html')


def opcoes_admin(request):
    return render(request, 'opcoes_admin.html')


def logout(request):
    return render(request, 'login.html')


def exibir_ajuda(request):
    return render(request, 'ajuda.html')


def editar_item(request):
    return None


def login(request):
    return render(request, 'login.html')


def exibir_um_equipamento(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'exibir_um_equipamento.html', {'item': item})
