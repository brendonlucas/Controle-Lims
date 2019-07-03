from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.decorators import *
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from controle.forms import *
from controle.models import *


def home(request):
    return render(request, 'home.html',
                  {'emprestimos': Emprestimo.objects.all(), 'user_logado': get_usuario_logado(request)})


# @login_required
def get_usuario_logado(request):
    return request.user


# @login_required
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
                new = Item(nome=nome, quantidade=qtd, tipo=tipo, imagem=image)
                new.save()
                return redirect('equipamentos')

        elif request.method == 'GET':
            return render(request, 'equipamentos/adicionar.html',
                          {'form': form, 'user_logado': get_usuario_logado(request)})
    else:
        return render(request, 'emprestimos.html', {'emprestimos': Emprestimo.objects.all(),
                                                    'user_logado': get_usuario_logado(request)})


# @login_required
def exibir_equipamentos(request):
    return render(request, 'equipamentos/listar.html',
                  {'itens': Item.objects.all(), 'user_logado': get_usuario_logado(request)})


# @login_required
def exibir_emprestimos(request):
    return render(request, 'emprestimos.html', {'user_logado': get_usuario_logado(request)})


# @login_required
def opcoes_admin(request):
    return render(request, 'opcoes_admin.html', {'user_logado': get_usuario_logado(request)})


# @login_required
def exibir_ajuda(request):
    return render(request, 'ajuda.html', {'user_logado': get_usuario_logado(request)})


# @login_required
def editar_item(request):
    return render(request, 'equipamentos/editar.html',
                  {'itens': Item.objects.all(), 'user_logado': get_usuario_logado(request)})


# @login_required
def exibir_um_equipamento(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'equipamentos/exibir.html', {'item': item, 'user_logado': get_usuario_logado(request)})


# @login_required
# @method_decorator(permission_required('user.is_superuser'), name='dispatch')
def excluir_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('equipamentos')


@method_decorator(permission_required('user.is_superuser'), name='dispatch')
class Editar(UpdateView):
    template_name = "equipamentos/editar.html"
    model = Item
    fields = '__all__'
    context_object_name = 'item'
    success_url = reverse_lazy("equipamentos")

