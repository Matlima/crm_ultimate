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

@app.route('/add_plan', methods=['POST'])
def created_plan():
    form = FormPlano(request.form)
    nome = form.nome.data
    descricao = form.descricao.data
    periodicidade = form.periodicidade.data
    preco = form.preco.data
    status = form.status.data
    novo_plano = Plano(nome=nome, descricao=descricao, preco=preco, status=status, periodicidade=periodicidade)
    db.session.add(novo_plano)
    db.session.commit()
    flash('Plano adicionado com sucesso!')
    return redirect(url_for('plan'))
