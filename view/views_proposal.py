from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Activity, User, Customer, Prospect, Proposal, ItemProposta, Plan
from helpers.forms_helpers import FormActivity, is_admin, FormProposal, FormItemProposta
from datetime import datetime

## Methods Routes:

@app.route('/proposal')
def proposal():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('proposal')))

    adm = is_admin()
    form = FormProposal()

    # Pegando o cliente e prospect dos parâmetros de busca (opcional)
    cliente_id = request.args.get('cliente_id', type=int)
    prospect_id = request.args.get('prospect_id', type=int)
    search = request.args.get('search', '')

    page = request.args.get('page', 1, type=int)

    # Construção da query, especificando o onclause no join para evitar ambiguidade
    query = db.session.query(Proposal).join(Customer, Proposal.customer_id == Customer.id)

    # Join explícito com a tabela User usando a chave estrangeira 'usuario_id'
    # query = query.join(User, Proposal.usuario_id == User.id)
    query = query.join(User, Proposal.responsavel_id == User.id, isouter=True)  # Join com 'responsavel_id' (opcional)

    # Aplicar filtro de busca se disponível
    if cliente_id:
        query = query.filter(Proposal.customer_id == cliente_id)

    if search:
        query = query.filter(Proposal.nome.ilike(f'%{search}%'))  # Busca por nome

    propostas = query.order_by(Proposal.data_criacao.desc()).paginate(page=page, per_page=10)

    return render_template('proposal/proposals.html',
                           titulo='Propostas Comerciais',
                           propostas=propostas,
                           clientes=Customer.query.all(),
                           prospects=Prospect.query.all(),
                           is_admin=adm,
                           form=form
                           )

@app.route('/proposal/add', methods=['GET', 'POST'])
def new_proposal():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('proposal')))

    adm = is_admin()
    form = FormProposal()

    # Preencher os choices para cliente e responsável
    form.customer_id.choices = [(cliente.id, cliente.razao_social) for cliente in Customer.query.all()]
    form.responsavel_id.choices = [(user.id, user.nome) for user in User.query.all()]

    if form.validate_on_submit():
        nova_proposta = Proposal(
            customer_id=form.customer_id.data,
            responsavel_id=form.responsavel_id.data,
            nome=form.nome.data,
            valor_total=form.valor_total.data,
            valor_total_service=form.valor_total_service.data,
            valor_total_plan=form.valor_total_plan.data,
            valor_total_product=form.valor_total_product.data,
            condicoes_pagamento=form.condicoes_pagamento.data,
            condicoes_comerciais=form.condicoes_comerciais.data,
            disposicao_gerais=form.disposicao_gerais.data,
            status=form.status.data
        )
        db.session.add(nova_proposta)
        db.session.commit()
        flash('Proposta criada com sucesso!')
        return redirect(url_for('proposal'))

    return render_template('proposal/add_proposal.html',
                           form=form,
                           is_admin=adm
                           )

@app.route('/proposal/add', methods=['GET', 'POST'])
def created_proposal():
    form = FormProposal()

    # Preenchendo os choices para os selects
    form.customer_id.choices = [(cliente.id, cliente.razao_social) for cliente in Customer.query.all()]
    form.responsavel_id.choices = [(responsavel.id, responsavel.nome) for responsavel in User.query.all()]

    # Log para verificar o método da requisição
    print("Método da requisição:", request.method)

    # Log para verificar se a sessão contém o usuario_id
    if "usuario_id" in session:
        print("Usuário logado ID:", session["usuario_id"])
    else:
        print("Nenhum usuário logado encontrado na sessão!")

    if form.validate_on_submit():
        try:
            print("Formulário validado com sucesso.")
            # Criar a proposta com os dados do formulário
            nova_proposta = Proposal(
                customer_id=form.customer_id.data,
                usuario_id=session.get("usuario_id"),  # Obtém o id do usuário da sessão
                responsavel_id=form.responsavel_id.data,
                data_criacao=datetime.now(),  # A data de criação será capturada automaticamente
                nome=form.nome.data,
                valor_total=form.valor_total.data,
                valor_total_service=form.valor_total_service.data,
                valor_total_plan=form.valor_total_plan.data,
                valor_total_product=form.valor_total_product.data,
                condicoes_pagamento=form.condicoes_pagamento.data,
                condicoes_comerciais=form.condicoes_comerciais.data,
                disposicao_gerais=form.disposicao_gerais.data,
                status=form.status.data
            )
            db.session.add(nova_proposta)
            db.session.commit()
            flash("Proposta criada com sucesso!")
            print("Proposta criada com sucesso.")
            return redirect(url_for('proposal'))

        except Exception as e:
            db.session.rollback()  # Em caso de erro, reverte a transação no banco
            flash(f"Ocorreu um erro ao criar a proposta: {str(e)}", "danger")
            print(f"Erro ao inserir no banco: {e}")
    else:
        # Se o formulário não validar, exibe os erros no console para depuração
        print("Erros de validação:", form.errors)
        flash("Erro na validação do formulário.", "danger")

    return render_template('proposal/add_proposal.html',
                           form=form
                           )

@app.route('/proposal/edit/<int:id>', methods=['GET', 'POST'])
def edit_proposal(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))

    proposta = Proposal.query.filter_by(id=id).first()
    page = request.args.get('page', 1, type=int)
    items_proposta = ItemProposta.query.filter_by(proposta_id=id).paginate(page=page, per_page=10)
    plans = Plan.query.all()

    form = FormProposal()
    formItemProposta = FormItemProposta()

    form.responsavel_id.choices = [(user.id, user.nome) for user in User.query.all()]
    form.customer_id.choices = [(customer.id, customer.razao_social) for customer in Customer.query.all()]
    form.process()

    formItemProposta.plan_id.choices = [(plan.id, plan.nome) for plan in plans]
    formItemProposta.process()

    form.customer_id.data = proposta.customer_id
    form.responsavel_id.data = proposta.responsavel_id

    form.status.data = proposta.status
    form.nome.data = proposta.nome
    form.valor_total.data = proposta.valor_total
    form.valor_total_service.data = proposta.valor_total_service
    form.valor_total_plan.data = proposta.valor_total_plan
    form.valor_total.data = proposta.valor_total
    form.condicoes_pagamento.data = proposta.condicoes_pagamento
    form.condicoes_comerciais.data = proposta.condicoes_comerciais
    form.disposicao_gerais.data = proposta.disposicao_gerais
    form.valor_total_product.data = proposta.valor_total_product

    adm = is_admin()
    return render_template('proposal/info_proposal.html',
                           id=id,
                           form=form,
                           formItemProposta=formItemProposta,
                           adm=adm,
                           items_proposta=items_proposta,
                           plans=plans
                           )



# --------------------------------
# ItemProposta:

@app.route('/proposal/<int:id>/item/create', methods=['GET', 'POST'])
def created_item_proposta(id):
    formItem = FormItemProposta()

    # Preenche os choices para os selects
    proposta = Proposal.query.get(id)
    # formItem.proposta_id.choices = [(proposta.id, proposta.nome)]
    formItem.plan_id.choices = [(plano.id, plano.nome) for plano in Plan.query.all()]

    if formItem.validate_on_submit():
        # Criar um novo ItemProposta com os dados do formulário
        novo_item = ItemProposta(
            proposta_id=proposta.id,
            plan_id=formItem.plan_id.data,
            quantidade=formItem.quantidade.data,
            desconto=formItem.desconto.data,
            total=formItem.total.data
        )
        db.session.add(novo_item)
        db.session.commit()
        flash("Item adicionado à proposta com sucesso!")
        return redirect(url_for('edit_proposal', id=id))
    else:
        print("Erros de validação do formulário:", formItem.errors)
        flash(f"Erro ao adicionar o item da proposta: {formItem.errors}", "danger")

    return redirect(url_for('edit_proposal', id=id))

@app.route('/proposal/<int:id>/item/edit/<int:id_item>/', methods=['GET', 'POST'])
def edit_item_proposal(id, id_item):
    usuario_id = session.get('usuario_id')
    usuario = User.query.get(usuario_id)
    proposta = Proposal.query.get(id)
    item_proposta = ItemProposta.query.get(id_item)

    formItem = FormItemProposta()
    formItem.plan_id.choices = [(plano.id, plano.nome) for plano in Plan.query.all()]

    if request.method == 'GET':
        if item_proposta:
            formItem.plan_id.data = item_proposta.plan_id
            formItem.quantidade.data = item_proposta.quantidade
            formItem.total.data = item_proposta.total
            formItem.desconto.data = item_proposta.desconto

        # Retorna o template edit_item.html com o ID do item
        return render_template('proposal/edit_item.html', formItemProposta=formItem, id=id, id_item=id_item)

    if request.method == 'POST' and formItem.validate_on_submit():
        item_proposta.plan_id = formItem.plan_id.data
        item_proposta.quantidade = formItem.quantidade.data
        item_proposta.desconto = formItem.desconto.data
        item_proposta.total = formItem.total.data
        db.session.commit()
        flash('Item atualizado com sucesso!')
        return redirect(url_for('edit_proposal', id=id))

    return redirect(url_for('edit_proposal', id=id))


## Methods Actions:

@app.route('/proposal/delete/<int:id>', methods=['GET', 'POST'])
def delete_proposal(id):
    usuario_id = session['usuario_id']
    usuario = User.query.filter_by(id=usuario_id).first()
    proposta = Proposal.query.filter_by(id=id).first()

    # Verificar se a proposta existe
    if not proposta:
        flash('Proposta não encontrada.', 'danger')
        return redirect(url_for('proposal'))

    # Verificar permissões de exclusão
    if usuario.grupo == 'Administrador' or proposta.responsavel_id == usuario.id:
        # Verificar se há itens associados à proposta
        if proposta.items_proposta:
            flash('Não é possível excluir a proposta, pois há itens associados.', 'danger')
        else:
            # Excluir a proposta, pois não há itens associados
            Proposal.query.filter_by(id=id).delete()
            db.session.commit()
            flash('Proposta excluída com sucesso!', 'success')
    else:
        flash('O usuário logado não tem autorização para excluir a proposta, apenas administradores ou o responsável.', 'danger')

    return redirect(url_for('proposal'))



# --------------------------------
# ItemProposta:
@app.route('/proposal/<int:id>/item/delete/<int:id_item>', methods=['GET', 'POST'])
def delete_item_proposal(id, id_item):
    usuario_id = session['usuario_id']
    usuario = User.query.filter_by(id=usuario_id).first()
    proposta = Proposal.query.filter_by(id=id).first()
    item_proposta = ItemProposta.query.filter_by(id=id_item)

    # Verificar se a proposta existe
    if not proposta:
        flash('Proposta não encontrada.', 'danger')
        return redirect(url_for('edit_proposal', id=id))

    # Verificar permissões de exclusão
    if usuario.grupo == 'Administrador' or proposta.responsavel_id == usuario.id:
        # Excluir o item da proposta
        ItemProposta.query.filter_by(id=id_item).delete()
        db.session.commit()
        flash('Item excluído com sucesso!', 'success')
    else:
        flash('O usuário logado não tem autorização para excluir o item da proposta, apenas administradores ou o responsável.', 'danger')

    return redirect(url_for('edit_proposal', id=id))