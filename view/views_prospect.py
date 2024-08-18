from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.prospect import Prospect
from helpers.helpers_forms import is_admin, FormProspect
from templates.customers import *
from uploads import *
from datetime import datetime

@app.route('/prospect')
def prospect():
    lista = Prospect.query.order_by(Prospect.id)
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('dashboard')))
    adm = is_admin()
    return render_template('prospects/prospects.html',  prospects=lista, is_admin=adm)

@app.route('/prospect/new')
def new_prospect():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormProspect()
    return render_template('prospects/add_prospect.html', form=form)

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