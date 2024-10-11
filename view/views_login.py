from application import app
from flask import render_template, request, redirect, session, flash, url_for
from models.models import User
from helpers.forms_helpers import FormUser, is_admin
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormUser()
    # form = FormularioUsuario()
    # return render_template('home.html', proxima=proxima, form=form)
    return render_template('auth/home.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormUser(request.form)
    usuario = User.query.filter_by(login=form.login.data).first()
    if not usuario:
        flash('Usuário não registrado.')
        return redirect(url_for('login'))
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session['usuario_logado'] = usuario.nome
        session['usuario_id'] = usuario.id
        if usuario.ativo == 'Ativo':
            flash(usuario.nome + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário desativado.')
            return redirect(url_for('login'))
    else:
        flash('Usuário e/ou senha incorreto(a).')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))


"""
@app.route('/home')
def home():
    proxima = request.args.get('proxima')
    form = FormUser()
    return render_template('home.html', proxima=proxima, form=form)
"""