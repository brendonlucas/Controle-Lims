from datetime import date
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from controle.models import Item

from emprestimo.forms import *
from emprestimo.models import *


def get_usuario_logado(request):
    return request.user


@login_required
def solicitar_item(request, item_id):
    form = FormQuantidade()
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        form = FormQuantidade(request.POST, request.FILES)
        if form.is_valid():
            qtd = form.cleaned_data['quantidade']
            descricao = form.cleaned_data['descricao']
            usuario = Usuario.objects.get(user=get_usuario_logado(request).id)
            if qtd <= item.quantidade:
                tipo = TipoEstadoEmprestimo.objects.get(id=1)
                data_atual = date.today()
                emprestimo = Emprestimo(equipamento=item, solicitante=usuario, data_emprestimo=data_atual, tipo=tipo,
                                        descricao=descricao, quantidade=qtd)
                emprestimo.save()
                return redirect('equipamentos')
            else:
                messages.error(request, 'Quantidade maior que a disponivel')
                return redirect('solicitar_emprestimo', item_id)
        else:
            messages.error(request, 'Prencha todos os campos!')
            return redirect('solicitar_emprestimo', item_id)

    elif request.method == 'GET':
        return render(request, 'pag_emprestimo.html',
                      {'form': form, 'user_logado': get_usuario_logado(request), 'item': item})


@login_required
def exibe_solicitacoes(request):
    if get_usuario_logado(request).is_superuser:
        solicitacoes = Emprestimo.objects.filter(tipo=1).order_by('data_emprestimo')
        paginator = Paginator(solicitacoes, 8)

        page = request.GET.get('page')
        solicitacoes = paginator.get_page(page)
        return render(request, 'pag_solicitacoes.html', {'emprestimos': solicitacoes,
                                                         'user_logado': get_usuario_logado(request)})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def aceita_solicitacao(request, solicitacao_id):
    if get_usuario_logado(request).is_superuser:
        solicitacao = Emprestimo.objects.get(id=solicitacao_id)
        solicitacao.tipo = TipoEstadoEmprestimo.objects.get(id=2)
        item = Item.objects.get(id=solicitacao.equipamento.id)
        qtd = item.quantidade
        if qtd >= solicitacao.quantidade:
            item.quantidade = qtd - solicitacao.quantidade
            item.save()
            solicitacao.save()
            return redirect('exibir_solicitacoes')
        else:
            messages.error(request, 'A quantidade de itens do pedido é maior que a disponivel:')
            return redirect('pag_falha')
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def rejeita_solicitacao(request, solicitacao_id):
    if get_usuario_logado(request).is_superuser:
        form = FromComentarioRejeitado()
        solicitacao = Emprestimo.objects.get(id=solicitacao_id)
        if request.method == 'POST':
            form = FromComentarioRejeitado(request.POST, request.FILES)
            if form.is_valid():
                coment = form.cleaned_data['comentario']
                solicitacao.mensagem_rejeitado = coment
                solicitacao.tipo = TipoEstadoEmprestimo.objects.get(id=3)
                solicitacao.estado = 1
                solicitacao.save()
                return redirect('exibir_solicitacoes')
            else:
                messages.error(request, 'Prencha todos os campos!')
                return redirect('rejeita_solicitacao', solicitacao_id)

        elif request.method == 'GET':
            return render(request, 'pag_rejeitar.html',
                          {'form': form, 'emprestimo': solicitacao, 'user_logado': get_usuario_logado(request)})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def pag_falha(request):
    return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def exibir_emprestimos(request):
    emprestimos_ativos = Emprestimo.objects.filter(tipo=2).order_by('-data_emprestimo')
    paginator = Paginator(emprestimos_ativos, 8)
    page = request.GET.get('page')
    emprestimos_ativos = paginator.get_page(page)
    return render(request, 'emprestimos.html',
                  {'emprestimos': emprestimos_ativos,
                   'user_logado': get_usuario_logado(request)})


@login_required
def exibir_detalhes(request, solicitacao_id):
    solicitacao = Emprestimo.objects.get(id=solicitacao_id)
    return render(request, 'pag_detalhes.html',
                  {'user_logado': get_usuario_logado(request), 'solicitacao': solicitacao})


@login_required
def fazer_devolucao_normal(request, emprestimo_id):
    if get_usuario_logado(request).is_superuser:
        emprestimo = Emprestimo.objects.get(id=emprestimo_id)
        equipamento = Item.objects.get(id=emprestimo.equipamento.id)
        equipamento.quantidade = equipamento.quantidade + emprestimo.quantidade
        equipamento.save()
        emprestimo.data_devolucao = date.today()
        emprestimo.tipo_id = 4
        emprestimo.save()
        return redirect('emprestimos')
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def fazer_devolucao_parcial(request, emprestimo_id):
    if get_usuario_logado(request).is_superuser:
        form = FormQuantidade()
        emprestimo = Emprestimo.objects.get(id=emprestimo_id)
        if request.method == 'GET':
            return render(request, 'pag_devolucao_parcial.html',
                          {'form': form, 'user_logado': get_usuario_logado(request), 'emprestimo': emprestimo})
        elif request.method == 'POST':
            form = FormQuantidade(request.POST)
            if form.is_valid():
                equipamento = Item.objects.get(id=emprestimo.equipamento.id)
                qtd = form.cleaned_data['quantidade']

                descricao = form.cleaned_data['descricao']
                if qtd <= emprestimo.quantidade:
                    equipamento.quantidade = equipamento.quantidade + qtd
                    equipamento.save()
                    emprestimo.mensagem_devolucao = descricao
                    emprestimo.data_devolucao = date.today()
                    emprestimo.tipo_id = 4
                    emprestimo.save()
                    return redirect('emprestimos')
                else:
                    messages.error(request, 'Quantidade maior que a disponivel no pedido')
                    return redirect('item_devolvido_parcial', emprestimo_id)
            else:
                messages.error(request, 'Prencha todos os campos!')
                return redirect('item_devolvido_parcial', emprestimo_id)
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def exibir_emprestimos_finalizados(request):
    emprestimos_finalizados = Emprestimo.objects.filter(tipo=4).order_by('-data_devolucao')
    paginator = Paginator(emprestimos_finalizados, 8)
    page = request.GET.get('page')
    emprestimos_finalizados = paginator.get_page(page)
    return render(request, 'pag_emp_finalizados.html',
                  {'emprestimos': emprestimos_finalizados, 'user_logado': get_usuario_logado(request)})


@login_required
def reservar_equipamento(request, item_id):
    if get_usuario_logado(request).is_superuser:
        form = FormQuantidade()
        item = Item.objects.get(id=item_id)
        if request.method == 'POST':
            form = FormQuantidade(request.POST, request.FILES)
            if form.is_valid():
                qtd = form.cleaned_data['quantidade']
                descricao = form.cleaned_data['descricao']
                usuario = Usuario.objects.get(user=get_usuario_logado(request).id)
                if qtd <= item.quantidade:
                    tipo = TipoEstadoEmprestimo.objects.get(id=2)
                    item.quantidade = item.quantidade - qtd
                    data_atual = date.today()
                    emprestimo = Emprestimo(equipamento=item, solicitante=usuario, data_emprestimo=data_atual,
                                            tipo=tipo,
                                            descricao=descricao, quantidade=qtd)
                    emprestimo.save()
                    item.save()
                    return redirect('equipamentos')
                else:
                    messages.error(request, 'Quantidade maior que a disponivel')
                    return redirect('solicitar_emprestimo', item_id)
            else:
                messages.error(request, 'Prencha todos os campos!')
                return redirect('solicitar_emprestimo', item_id)

        elif request.method == 'GET':
            return render(request, 'pag_emprestimo.html',
                          {'form': form, 'user_logado': get_usuario_logado(request), 'item': item})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})