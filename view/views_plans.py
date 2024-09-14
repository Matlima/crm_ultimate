from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Plan
from helpers.helpers_forms import is_admin, FormPlano
from templates.customers import *
from uploads import *
from datetime import datetime


@app.route('/plans')
def plan():
    lista = Plan.query.order_by(Plan.id)
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('dashboard')))
    adm = is_admin()
    return render_template('plans/plans.html',  plans=lista, is_admin=adm)

@app.route('/plans/new')
def new_plan():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormPlano()
    return render_template('plans/add_plan.html', form=form)

@app.route('/plans/category/new')
def new_category_plan():
    pass

@app.route('/plans/add', methods=['POST'])
def created_plan():
    form = FormPlano(request.form)
    nome = form.nome.data
    descricao = form.descricao.data
    periodicidade = form.periodicidade.data
    preco = form.preco.data
    status = form.status.data
    novo_plano = Plan(nome=nome, descricao=descricao, preco=preco, status=status, periodicidade=periodicidade)
    db.session.add(novo_plano)
    db.session.commit()
    flash('Plan adicionado com sucesso!')
    return redirect(url_for('plan'))


@app.route('/plans/edit/<int:id>')
def edit_plan(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    plan = Plan.query.filter_by(id=id).first()
    form = FormPlano()
    form.nome.data = plan.nome
    form.status.data = plan.status
    form.descricao.data = plan.descricao
    form.preco.data = plan.preco
    form.periodicidade.data = plan.periodicidade
    return render_template('plans/edit_plan.html', id=id, form=form)


@app.route('/plans/update', methods=['POST'])
def update_plan():
    form = FormPlano(request.form)
    plan = Plan.query.filter_by(id=request.form['id']).first()
    if form.validate_on_submit():
        if plan:
            plan.nome = form.nome.data
            plan.status = form.status.data
            plan.descricao = form.descricao.data
            plan.preco = form.preco.data
            plan.periodicidade = form.periodicidade.data
            db.session.commit()
            flash('Plan atualizado com sucesso', 'sucess')
            return redirect(url_for('plan'))
        else:
            flash('Plano não encontrado', 'error')
            return redirect(url_for('edit_plan', id=request.form['id']))

