from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Activity, User, Customer, Prospect, Proposal
from helpers.forms_helpers import FormActivity, is_admin, FormProposal
from datetime import datetime

@app.route('/proposta/nova', methods=['GET', 'POST'])
def created_proposal():
    form = FormProposal()

    # Preenchendo os choices para os selects
    form.customer_id.choices = [(cliente.id, cliente.nome) for cliente in Customer.query.all()]
    form.usuario_id.choices = [(usuario.id, usuario.nome) for usuario in User.query.all()]
    form.responsavel_id.choices = [(responsavel.id, responsavel.nome) for responsavel in User.query.all()]

    if form.validate_on_submit():
        # Criar a proposta com os dados do formulário
        nova_proposta = Proposal(
            customer_id=form.customer_id.data,
            usuario_id=form.usuario_id.data,
            responsavel_id=form.responsavel_id.data,
            data_criacao=form.data_criacao.data,
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
        return redirect(url_for('lista_propostas'))

    return render_template('proposta/nova.html', form=form)