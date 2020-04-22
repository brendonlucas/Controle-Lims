from datetime import date
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from emprestimo.forms import *
from emprestimo.models import *


def get_usuario_logado(request):
    return request.user


def get_qtd_notificacoes():
    return Emprestimo.objects.filter(visualisado=0).count()


@login_required
def confirmar_visualizacao(request, emprestimo_id):
    if get_usuario_logado(request).is_superuser:
        emprestimo = Emprestimo.objects.get(id=emprestimo_id)
        emprestimo.visualisado = True
        emprestimo.save()
        return redirect('exibir_notificacoes')


def emprestimos_ativos(request):
    lista_emprestimos_ativos = Emprestimo.objects.filter(tipo=1).order_by('-data_emprestimo')

    paginator = Paginator(lista_emprestimos_ativos, 8)
    page = request.GET.get('page')
    lista_emprestimos_ativos = paginator.get_page(page)
    return render(request, 'pag_todos_os_emprestimos.html', {'emprestimos': lista_emprestimos_ativos,
                                                             'user_logado': get_usuario_logado(request),
                                                             'qtd_notificacoes': get_qtd_notificacoes()})


def emprestimos_finalizados(request):
    lista_emprestimos_finalizados = Emprestimo.objects.filter(tipo=2).order_by('-data_emprestimo')

    paginator = Paginator(lista_emprestimos_finalizados, 8)
    page = request.GET.get('page')
    lista_emprestimos_finalizados = paginator.get_page(page)
    return render(request, 'pag_todos_os_emprestimos.html', {'emprestimos': lista_emprestimos_finalizados,
                                                             'user_logado': get_usuario_logado(request),
                                                             'qtd_notificacoes': get_qtd_notificacoes()})


"""
@login_required
def exibe_solicitacoes(request):
    if get_usuario_logado(request).is_superuser:
        solicitacoes = Emprestimo.objects.filter(visualisado=0).order_by('data_emprestimo')

        paginator = Paginator(solicitacoes, 8)
        page = request.GET.get('page')
        solicitacoes = paginator.get_page(page)
        return render(request, 'pag_solicitacoes.html', {'emprestimos': solicitacoes,
                                                         'user_logado': get_usuario_logado(request),
                                                         'qtd_notificacoes': get_qtd_notificacoes()})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def aceita_solicitacao(request, solicitacao_id):
    if get_usuario_logado(request).is_superuser:
        solicitacao = Emprestimo.objects.get(id=solicitacao_id)
        item = Item.objects.get(id=solicitacao.equipamento.id)
        qtd = item.quantidade

        if solicitacao.tipo.id != 5:
            if qtd >= solicitacao.quantidade:
                solicitacao.tipo = TipoEstadoEmprestimo.objects.get(id=2)
                item.quantidade = qtd - solicitacao.quantidade
                item.quantidade_emprestada = item.quantidade_emprestada + solicitacao.quantidade
                item.save()
                solicitacao.save()
                return redirect('exibir_solicitacoes')
            else:
                messages.error(request, 'A quantidade de itens do pedido é maior que a disponivel:')
                return redirect('pag_falha')
        elif solicitacao.tipo.id == 5:
            solicitacao.tipo = TipoEstadoEmprestimo.objects.get(id=6)
            solicitacao.save()
            return redirect('exibir_solicitacoes')
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def exibir_detalhes_solicitacao(request, solicitacao_id):
    try:
        solicitacao = Emprestimo.objects.get(id=solicitacao_id)

    except Emprestimo.DoesNotExist:
        messages.error(request, 'Não encontrado!!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})

    if solicitacao.tipo.id == 1 or solicitacao.tipo.id == 5:
        return render(request, 'pag_detalhes.html',
                      {'user_logado': get_usuario_logado(request), 'solicitacao': solicitacao})
    else:
        messages.error(request, 'Não encontrado!')
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
def exibir_emprestimos_2(request):
    emprestimos_ativos = Emprestimo.objects.filter(tipo=2).order_by('-data_emprestimo')
    paginator = Paginator(emprestimos_ativos, 8)
    page = request.GET.get('page')
    emprestimos_ativos = paginator.get_page(page)
    return render(request, 'emprestimos.html',
                  {'emprestimos': emprestimos_ativos,
                   'user_logado': get_usuario_logado(request)})
"""


# nova_funcao
@login_required
def exibe_notificacoes_emprestimos(request):
    # print(Item.objects.filter(nome__contains="Ardu"))
    if get_usuario_logado(request).is_superuser:
        solicitacoes = Emprestimo.objects.filter(visualisado=0).order_by('data_emprestimo')
        paginator = Paginator(solicitacoes, 8)
        page = request.GET.get('page')
        solicitacoes = paginator.get_page(page)
        return render(request, 'pag_solicitacoes.html', {'emprestimos': solicitacoes,
                                                         'user_logado': get_usuario_logado(request),
                                                         'qtd_notificacoes': get_qtd_notificacoes()})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


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
                item.quantidade = item.quantidade - qtd
                item.quantidade_emprestada = item.quantidade_emprestada + qtd
                item.save()
                emprestimo.save()
                return redirect('equipamentos')
            else:
                messages.error(request, 'Quantidade maior que a disponivel')
                return redirect('solicitar_emprestimo', item_id)
        else:
            messages.error(request, 'Prencha todos os campos corretamente')
            return redirect('solicitar_emprestimo', item_id)

    elif request.method == 'GET':
        return render(request, 'pag_emprestimo.html',
                      {'form': form, 'user_logado': get_usuario_logado(request), 'item': item,
                       'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def exibir_emprestimos(request):
    usuario_logado = Usuario.objects.get(user=get_usuario_logado(request).id)
    emprestimos_ativos = Emprestimo.objects.filter(tipo=1).filter(solicitante=usuario_logado.id).order_by(
        '-data_emprestimo')
    paginator = Paginator(emprestimos_ativos, 8)
    page = request.GET.get('page')
    emprestimos_ativos = paginator.get_page(page)
    return render(request, 'emprestimos.html', {'emprestimos': emprestimos_ativos,
                                                'user_logado': get_usuario_logado(request),
                                                'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def exibir_emprestimos_finalizados(request):
    usuario_logado = Usuario.objects.get(user=get_usuario_logado(request).id)
    emprestimos_finalizados = Emprestimo.objects.filter(tipo=2).filter(solicitante=usuario_logado.id).order_by(
        '-data_emprestimo')
    paginator = Paginator(emprestimos_finalizados, 8)
    page = request.GET.get('page')
    emprestimos_ativos = paginator.get_page(page)
    return render(request, 'emprestimos.html', {'emprestimos': emprestimos_ativos,
                                                'user_logado': get_usuario_logado(request),
                                                'qtd_notificacoes': get_qtd_notificacoes()})


def exibir_todos_emporestimos_ativos():
    pass


def exibir_todos_emporestimos_finalizados():
    pass


@login_required
def exibir_detalhes(request, emprestimo_id):
    try:
        solicitacao = Emprestimo.objects.get(id=emprestimo_id)
    except Emprestimo.DoesNotExist:
        messages.error(request, 'Não encontrado!!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})

    return render(request, 'pag_detalhes.html', {'user_logado': get_usuario_logado(request),
                                                 'solicitacao': solicitacao,
                                                 'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def fazer_devolucao_normal(request, emprestimo_id):
    if get_usuario_logado(request).is_superuser:
        try:
            emprestimo = Emprestimo.objects.get(id=emprestimo_id)
            equipamento = Item.objects.get(id=emprestimo.equipamento.id)

        except Emprestimo.DoesNotExist:
            messages.error(request, 'Emprestimo não encontrado')
            return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})

        equipamento.quantidade = equipamento.quantidade + emprestimo.quantidade
        equipamento.quantidade_emprestada = equipamento.quantidade_emprestada - emprestimo.quantidade
        equipamento.save()
        emprestimo.data_devolucao = date.today()
        emprestimo.tipo_id = 2
        emprestimo.save()

        lista_reserva = Emprestimo.objects.filter(tipo=6).order_by('id')
        if len(lista_reserva) > 0:
            for i in range(len(lista_reserva)):
                reserva = lista_reserva[i]
                if equipamento.quantidade >= reserva.quantidade:
                    equipamento.quantidade = equipamento.quantidade - reserva.quantidade
                    equipamento.quantidade_emprestada = equipamento.quantidade_emprestada + reserva.quantidade
                    reserva.tipo = TipoEstadoEmprestimo.objects.get(id=2)
                    equipamento.save()
                    reserva.save()

        return redirect('emprestimos')
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def fazer_devolucao_parcial(request, emprestimo_id):
    if get_usuario_logado(request).is_superuser:
        try:
            emprestimo = Emprestimo.objects.get(id=emprestimo_id)
            equipamento = Item.objects.get(id=emprestimo.equipamento.id)

        except Emprestimo.DoesNotExist:
            messages.error(request, 'Emprestimo não encontrado')
            return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})

        form = FormQuantidadeDevolucao()
        if request.method == 'GET':
            return render(request, 'pag_devolucao_parcial.html',
                          {'form': form, 'user_logado': get_usuario_logado(request), 'emprestimo': emprestimo})

        elif request.method == 'POST':
            form = FormQuantidadeDevolucao(request.POST)
            if form.is_valid():
                qtd = form.cleaned_data['quantidade']
                quantidade_defeituoso = form.cleaned_data['quantidade_defeituoso']
                descricao = form.cleaned_data['descricao']

                if quantidade_defeituoso + qtd > emprestimo.quantidade or \
                        quantidade_defeituoso + qtd < emprestimo.quantidade:
                    messages.error(request, 'Quantidades Invalidas!')
                    return redirect('item_devolvido_parcial', emprestimo_id)

                if qtd <= emprestimo.quantidade:
                    equipamento.quantidade = equipamento.quantidade + qtd
                    equipamento.quantidade_emprestada = equipamento.quantidade_emprestada - emprestimo.quantidade
                    equipamento.quantidade_descartada = equipamento.quantidade_descartada + quantidade_defeituoso

                    emprestimo.mensagem_devolucao = descricao
                    emprestimo.data_devolucao = date.today()
                    emprestimo.tipo_id = 2
                    emprestimo.save()
                    equipamento.save()

                    lista_reserva = Emprestimo.objects.filter(tipo=6).order_by('id')
                    if len(lista_reserva) > 0:
                        for i in range(len(lista_reserva)):
                            reserva = lista_reserva[i]
                            if equipamento.quantidade >= reserva.quantidade:
                                equipamento.quantidade = equipamento.quantidade - reserva.quantidade
                                equipamento.quantidade_emprestada = equipamento.quantidade_emprestada + reserva.quantidade
                                reserva.tipo = TipoEstadoEmprestimo.objects.get(id=2)
                                equipamento.save()
                                reserva.save()

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
def reservar_equipamento(request, item_id):
    form = FormQuantidade()
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        form = FormQuantidade(request.POST, request.FILES)
        if form.is_valid():
            qtd = form.cleaned_data['quantidade']
            descricao = form.cleaned_data['descricao']
            usuario = Usuario.objects.get(user=get_usuario_logado(request).id)
            tipo = TipoEstadoEmprestimo.objects.get(id=5)

            data_atual = date.today()
            emprestimo = Emprestimo(equipamento=item, solicitante=usuario, data_emprestimo=data_atual,
                                    tipo=tipo, descricao=descricao, quantidade=qtd)
            emprestimo.save()
            return redirect('equipamentos')
        else:
            messages.error(request, 'Prencha todos os campos!')
            return redirect('solicitar_emprestimo', item_id)

    elif request.method == 'GET':
        return render(request, 'pag_emprestimo.html',
                      {'form': form, 'user_logado': get_usuario_logado(request), 'item': item})


@login_required
def pag_falha(request):
    return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request),
                                              'qtd_notificacoes': get_qtd_notificacoes()})
