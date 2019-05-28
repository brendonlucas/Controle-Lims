from controle.models import *
from django.shortcuts import render, redirect
from controle.forms import *


def home(request):
    return render(request, 'home.html', {'emprestimos': Emprestimo.objects.all()})


def add_equipamento(request):
    form = ItemForm()
    print("Aquiiiiii")
    print(request.method)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        print("leo")
        if form.is_valid():
            nome = form.cleaned_data['nome']
            qtd = form.cleaned_data['quantidade']
            tipo = form.cleaned_data['tipo']
            new = Item(nome=nome, telefone=qtd, tipo=tipo)
            new.save()
            return redirect('home')

    elif request.method == 'GET':
        return render(request, 'adicionar_equipamento.html', {'form': form})


def add_user(request):
    form = PostForm()
    print("fggff", request.POST)
    if request.method == 'POST':
        form = PostForm(request.POST)
        print(request.POST)
        if form.is_valid():
            user_nome = form.cleaned_data['nome']
            user_telefone = form.cleaned_data['telefone']
            user_tipo = form.cleaned_data['tipo']
            new_post = Usuario(nome=user_nome, telefone=user_telefone, tipo=user_tipo)
            new_post.save()
            return redirect('home')

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



def editar_item(request):
    return None


def login(request):
    return render(request, 'login.html')


def exibir_um_equipamento(request, equipamento_id):
    item = Item.objects.get(id=equipamento_id)
    return render(request, 'exibir_um_equipamento.html', {'item': item})