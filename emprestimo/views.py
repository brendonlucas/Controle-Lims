from datetime import date
from django.contrib import messages
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
            descricao = form.cleaned_data['descicao']
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
        solicitacoes = Emprestimo.objects.filter(tipo=1)
        return render(request, 'pag_solicitacoes.html', {'emprestimos': solicitacoes.order_by('data_emprestimo'),
                                                         'user_logado': get_usuario_logado(request)})
    else:
        redirect('emprestimos')


@login_required
def aceita_solicitacao(request, solicitacao_id):
    if get_usuario_logado(request).is_superuser:
        solicitacao = Emprestimo.objects.get(id=solicitacao_id)
        solicitacao.tipo = TipoEstadoEmprestimo.objects.get(id=2)
        solicitacao.save()
        return redirect('exibir_solicitacoes')
    else:
        redirect('emprestimos')


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
        return render(request,'emprestimos.html')


@login_required
def exibir_emprestimos(request):
    emprestimos_ativos = Emprestimo.objects.filter(tipo=2)
    return render(request, 'emprestimos.html',
                  {'emprestimos': emprestimos_ativos.order_by('-data_emprestimo'),
                   'user_logado': get_usuario_logado(request)})


@login_required
def exibir_detalhes(request, solicitacao_id):
    solicitacao = Emprestimo.objects.get(id=solicitacao_id)
    return render(request, 'pag_detalhes.html',
                  {'user_logado': get_usuario_logado(request), 'solicitacao': solicitacao})
