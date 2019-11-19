from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.decorators import *
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from controle.forms import *
from emprestimo.models import *
from controle.models import *


@login_required
def home(request):
    return render(request, 'home.html',
                  {'emprestimos': Emprestimo.objects.all(), 'user_logado': get_usuario_logado(request)})


def get_usuario_logado(request):
    return request.user


@login_required
def add_equipamento(request):
    if get_usuario_logado(request).is_superuser:
        form = ItemForm()
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                nome = form.cleaned_data['nome']
                qtd = form.cleaned_data['quantidade']
                tipo = form.cleaned_data['tipo']
                image = form.cleaned_data['imagem']
                if image is None:
                    image = 'documents/1111/sem_foto.jpg'
                new = Item(nome=nome, quantidade=qtd, tipo=tipo, imagem=image)
                new.save()
                return redirect('equipamentos')

        elif request.method == 'GET':
            return render(request, 'equipamentos/adicionar.html',
                          {'form': form, 'user_logado': get_usuario_logado(request)})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def exibir_equipamentos(request):

    itens = Item.objects.filter(excluido=False).exclude(quantidade=0)
    itens2 = Item.objects.filter(quantidade=0)

    itens = itens.union(itens2, all=True)

    paginator = Paginator(itens, 8)
    page = request.GET.get('page')
    itens = paginator.get_page(page)
    return render(request, 'equipamentos/listar.html',
                  {'itens': itens, 'user_logado': get_usuario_logado(request)})


@login_required
def opcoes_admin(request):
    if get_usuario_logado(request).is_superuser:
        return render(request, 'opcoes_admin.html', {'user_logado': get_usuario_logado(request)})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def exibir_ajuda(request):
    return render(request, 'ajuda.html', {'user_logado': get_usuario_logado(request)})


@login_required
def exibir_um_equipamento(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'equipamentos/exibir.html', {'item': item, 'user_logado': get_usuario_logado(request)})


@login_required
def excluir_item(request, item_id):
    if get_usuario_logado(request).is_superuser:
        item = Item.objects.get(id=item_id)
        item.excluido = True
        item.save()
        return redirect('equipamentos')
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def exibe_excluidos(request):
    if get_usuario_logado(request).is_superuser:
        itens = Item.objects.filter(excluido=True)
        return render(request, 'equipamentos/temp_removidos/excluidos.html',
                      {'user_logado': get_usuario_logado(request), 'itens': itens})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def item_editar(request, pk):
    if get_usuario_logado(request).is_superuser:
        item = get_object_or_404(Item, pk=pk)
        if request.method == "POST":
            form = ItemForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                item = form.save(commit=False)
                item.save()
                return redirect('equipamentos')
        else:
            form = ItemForm(instance=item)
        return render(request, 'equipamentos/adicionar.html', {'form': form, 'user_logado': get_usuario_logado(request)})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})