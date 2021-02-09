from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import *
from django.db.models.functions import Lower
from django.shortcuts import render, redirect, get_object_or_404
from controle.forms import *
from controle.models import *
from emprestimo.models import TipoEstadoEmprestimo, Emprestimo


def get_usuario_logado(request):
    return request.user


def get_qtd_notificacoes():
    return Emprestimo.objects.filter(visualisado=0).count()


def get_emprestimo_ativo():
    return Controle.objects.get(id=1).emprestimo_ativo


@login_required
def add_equipamento(request):
    if get_usuario_logado(request).is_superuser:
        form = ItemForm()
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                nome = form.cleaned_data['nome']
                qtd = form.cleaned_data['quantidade']
                tipo = TipoEquipamento.objects.get(nome=form.cleaned_data['tipo'])
                image = form.cleaned_data['imagem']
                if image is None:
                    image = 'documents/1111/sem_foto.jpg'

                new = Item(nome=nome, quantidade=qtd, tipo=tipo, imagem=image, quantidade_emprestada=0)
                if form.cleaned_data['codigo_tombamento'] is not None:
                    new.codigo_tombamento = form.cleaned_data['codigo_tombamento']
                    new.save()
                    return redirect('equipamentos')
            else:
                messages.error(request, 'Formulario imvalido!')
                return redirect('adicionar_equipamento')
        elif request.method == 'GET':
            return render(request, 'equipamentos/adicionar.html', {'form': form,
                                                                   'user_logado': get_usuario_logado(request),
                                                                   'qtd_notificacoes': get_qtd_notificacoes()})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def opcoes_admin(request):
    if get_usuario_logado(request).is_superuser:
        return render(request, 'opcoes_admin.html', {'user_logado': get_usuario_logado(request),
                                                     'qtd_notificacoes': get_qtd_notificacoes(),
                                                     'emprestimo_ativo': get_emprestimo_ativo()})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})


@login_required
def exibir_um_equipamento(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        messages.error(request, 'Item não encontrado!')
        return render(request, 'pag_falha.html', {'user_logado': get_usuario_logado(request)})

    emprestimos = Emprestimo.objects.filter(equipamento=item_id).filter(tipo=1)
    return render(request, 'equipamentos/exibir.html', {'item': item, 'user_logado': get_usuario_logado(request),
                                                        'emprestimos': emprestimos,
                                                        'qtd_notificacoes': get_qtd_notificacoes(),
                                                        'emprestimo_ativo': get_emprestimo_ativo()})


@login_required
def exibir_equipamentos(request):
    itens = Item.objects.filter(excluido=False).exclude(quantidade=0)
    itens2 = Item.objects.filter(quantidade=0).exclude(excluido=True)

    itens = itens.union(itens2, all=True).order_by('nome')

    paginator = Paginator(itens, 8)
    page = request.GET.get('page')
    itens = paginator.get_page(page)
    return render(request, 'equipamentos/listar.html',
                  {'itens': itens, 'user_logado': get_usuario_logado(request),
                   'qtd_notificacoes': get_qtd_notificacoes(),
                   'emprestimo_ativo': get_emprestimo_ativo()})


@login_required
def bloquear_emprestimos(request):
    if get_usuario_logado(request).is_superuser:
        controle = Controle.objects.get(id=1)
        if controle.emprestimo_ativo:
            controle.emprestimo_ativo = False
        else:
            controle.emprestimo_ativo = True
        controle.save()

        # equipamentos = Item.objects.all()
        # for equipamento in equipamentos:
        #   equipamento.bloqueado = True
        #   equipamento.save()

        return redirect("painel_admin")
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html',
                      {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})


"""
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
        
        
"""


@login_required
def exibe_excluidos(request):
    if get_usuario_logado(request).is_superuser:
        itens = Item.objects.filter(excluido=True)
        return render(request, 'equipamentos/temp_removidos/excluidos.html',
                      {'user_logado': get_usuario_logado(request), 'itens': itens,
                       'qtd_notificacoes': get_qtd_notificacoes()})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html',
                      {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def item_editar(request, pk):
    if get_usuario_logado(request).is_superuser:
        item = get_object_or_404(Item, pk=pk)
        if request.method == "POST":
            form = ItemFormEdit(request.POST, request.FILES, instance=item)
            if form.is_valid():
                item = form.save(commit=False)
                item.save()
                return redirect('equipamentos')
            else:
                return redirect('editar_equipamento', pk)
        else:
            form = ItemFormEdit(instance=item)
            return render(request, 'equipamentos/editar.html',
                          {'form': form, 'user_logado': get_usuario_logado(request),
                           'qtd_notificacoes': get_qtd_notificacoes()})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html',
                      {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def restaurar_item(request, item_id):
    if get_usuario_logado(request).is_superuser:
        item = Item.objects.get(id=item_id)
        item.excluido = False
        item.save()
        return redirect('itens_excluidos')
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html',
                      {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def mudar_status(request, item_id):
    if get_usuario_logado(request).is_superuser:
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            messages.error(request, 'Equipamento não existe!')
            return render(request, 'pag_falha.html',
                          {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})

        if request.method == 'POST':
            form = FormMudarStatus(request.POST)
            # print('sdasdasda', form.cleaned_data['status'])
            if form.is_valid():
                print('sdasdasda', form.cleaned_data['status'])
                if form.cleaned_data['status'] == 'Em Funcionamento':
                    item.em_operacao = True
                    item.save()
                elif form.cleaned_data['status'] == 'Com Problema':
                    item.em_operacao = False
                    item.save()

                return redirect('equipamentos')
            else:
                messages.error(request, 'Valor invalido!')
                return render(request, 'pag_falha.html',
                              {'user_logado': get_usuario_logado(request),
                               'qtd_notificacoes': get_qtd_notificacoes()})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html',
                      {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def add_unidades(request, item_id):
    if get_usuario_logado(request).is_superuser:
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            messages.error(request, 'Equipamento não existe!')
            return render(request, 'pag_falha.html',
                          {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})

        if request.method == 'POST':
            form = FormAddUnidade(request.POST)
            if form.is_valid():
                item.quantidade = item.quantidade + form.cleaned_data['quantidade']
                item.save()
                lista_reserva = Emprestimo.objects.filter(tipo=6).order_by('id')
                if len(lista_reserva) > 0:
                    for i in range(len(lista_reserva)):
                        reserva = lista_reserva[i]
                        if item.quantidade >= reserva.quantidade:
                            item.quantidade = item.quantidade - reserva.quantidade
                            item.quantidade_emprestada = item.quantidade_emprestada + reserva.quantidade
                            reserva.tipo = TipoEstadoEmprestimo.objects.get(id=2)
                            item.save()
                            reserva.save()
                return redirect('equipamentos')
            else:
                messages.error(request, 'Valor invalido!')
                return render(request, 'pag_falha.html',
                              {'user_logado': get_usuario_logado(request),
                               'qtd_notificacoes': get_qtd_notificacoes()})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html',
                      {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def relatorio_consumiveis(request):
    if get_usuario_logado(request).is_superuser:
        itens = Item.objects.filter(tipo_id=1)
        return render(request, 'relatorios/relatorio_consumivel.html',
                      {'itens': itens, 'user_logado': get_usuario_logado(request),
                       'qtd_notificacoes': get_qtd_notificacoes()})
    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html',
                      {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})


@login_required
def relatorio_permanentes(request):
    if get_usuario_logado(request).is_superuser:
        itens = Item.objects.filter(tipo_id=2)
        return render(request, 'relatorios/relatorio_permanente.html',
                      {'itens': itens, 'user_logado': get_usuario_logado(request),
                       'qtd_notificacoes': get_qtd_notificacoes()})

    else:
        messages.error(request, 'Acesso negado!')
        return render(request, 'pag_falha.html',
                      {'user_logado': get_usuario_logado(request), 'qtd_notificacoes': get_qtd_notificacoes()})
