from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Activity, User, Customer, Prospect, Proposal
from helpers.forms_helpers import FormActivity, is_admin, FormProposal
from datetime import datetime


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

    return render_template('proposal/add_proposal.html', form=form)


@app.route('/proposal/info/<int:id>', methods=['GET', 'POST'])
def info_proposal():
    pass

@app.route('/proposal/edit/<int:id>', methods=['GET', 'POST'])
def edit_proposal():
    pass

@app.route('/proposal/delete/<int:id>', methods=['GET', 'POST'])
def delete_proposal():
    pass

