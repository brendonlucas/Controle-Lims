from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

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
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            qtd = form.cleaned_data['quantidade']
            tipo = form.cleaned_data['tipo']
            image = form.cleaned_data['imagem']
            new = Item(nome=nome, quantidade=qtd, tipo=tipo, imagem=image)
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
    return user_login(request)


def exibir_ajuda(request):
    return render(request, 'ajuda.html')


def editar_item(request):
    return render(request, 'listar_items_editar.html', {'itens': Item.objects.all()})


def exibir_um_equipamento(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'exibir_um_equipamento.html', {'item': item})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def eeditar(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'editar_equipamento.html', {'item': item})


class Editar(UpdateView):
    template_name = "editar_equipamento.html"
    model = Item
    fields = '__all__'
    context_object_name = 'item'
    success_url = reverse_lazy("equipamentos")

