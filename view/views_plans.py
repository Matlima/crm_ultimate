from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.plano import Plano
from helpers.helpers_forms import is_admin, FormPlano
from templates.customers import *
from uploads import *
from datetime import datetime


@app.route('/plan')
def plan():
    lista = Plano.query.order_by(Plano.id)
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('dashboard')))
    adm = is_admin()
    return render_template('plans/plans.html',  plans=lista, is_admin=adm)

@app.route('/plan/new')
def new_plan():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormPlano()
    return render_template('plans/add_plan.html', form=form)

@app.route('/add_prospect', methods=['POST'])
def created_prospect():
    form = FormProspect(request.form)
    nome_completo = form.nome_completo.data
    email = form.email.data
    telefone = form.telefone.data
    observacao = form.observacao.data
    data_hora_cadastro = datetime.now()

    novo_prospect = Prospect(nome_completo=nome_completo, email=email, telefone=telefone,
                             observacao=observacao,data_hora_cadastro=data_hora_cadastro)
    db.session.add(novo_prospect)
    db.session.commit()
    flash('Prospect adicionado com sucesso!')
    return redirect(url_for('prospect'))
