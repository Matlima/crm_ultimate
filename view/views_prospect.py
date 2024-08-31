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


@app.route('/prospect/delete/<int:id>')
def delete_prospect(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))

    try:
        Prospect.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Prospect excluido com sucesso!')
    except InterruptedError:
        db.session.rollback()
        flash('Erro: Prospect está vinculado a outras atividades. Exclua as atividades relacionadas primeiro.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir prospect: {str(e)}", "error")

    return redirect(url_for('prospect'))


@app.route('/prospect/edit/<int:id>')
def edit_prospect(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    prospect = Prospect.query.filter_by(id=id).first()
    form = FormProspect()
    form.nome_completo.data = prospect.nome_completo
    form.telefone.data = prospect.telefone
    form.email.data = prospect.email
    form.observacao.data = prospect.observacao
    return render_template('prospects/edit_prospect.html', id=id, form=form)