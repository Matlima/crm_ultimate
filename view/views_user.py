from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from application import app, db
from models import User
from helpers import FormUser
from flask_bcrypt import generate_password_hash
from sqlalchemy.exc import IntegrityError



@app.route('/users')
def users():
    lista = User.query.order_by(User.id)
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('dashboard')))
    form = FormUser()
    return render_template('users.html', titulo='Usuários', usuarios=lista, form=form)


@app.route('/add_user')
def add_user():
    # Se ainda não salvou a sessão vai sempre voltar para o login
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormUser()
    return render_template('add_user.html', titulo='Novo usuário', form=form)


@app.route('/users/add', methods=['POST',])
def created_user():
    form = FormUser(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('register'))
    nome = form.nome.data
    email = form.email.data
    login = form.login.data
    senha = generate_password_hash(form.senha.data).decode('utf-8')
    grupo = form.grupo.data
    ativo = form.ativo.data
    telefone = form.telefone.data
    cargo = form.cargo.data
    setor = form.setor.data

    usuario = User.query.filter_by(login=login).first()

    if usuario:
        flash('Login indisponível, escolha outro')
        return redirect(url_for('register'))

    novo_usuario = User(nome=nome, email=email, login=login, senha=senha, grupo=grupo,
                           telefone=telefone, cargo=cargo, setor=setor, ativo=ativo)
    db.session.add(novo_usuario)
    db.session.commit()
    flash('Usuário adicionado com sucesso!', 'success')

    return redirect(url_for('users'))


# Edição de Usuário
@app.route('/user/edit/<int:id>')
def edit_user(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))

    user = User.query.filter_by(id=id).first()
    form = FormUser()
    form.nome.data = user.nome
    form.login.data = user.login
    form.email.data = user.email
    form.grupo.data = user.grupo
    form.telefone.data = user.telefone
    form.cargo.data = user.cargo
    form.setor.data = user.setor
    form.ativo.data = user.ativo

    return render_template('edit_user.html', titulo='Editando Usuário', id=id, form=form)

@app.route('/user/delete/<int:id>')
def delete_user(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proximo=url_for('novo')))

    try:
        # Tente excluir o usuário
        User.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Usuário excluído com sucesso!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Erro: Usuário está vinculado a outras atividades. Exclua as atividades relacionadas primeiro.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir usuário: {str(e)}", "error")

    return redirect(url_for('users'))

@app.route('/user/update', methods=['POST'])
def update_user():
    form = FormUser(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(id=request.form['id']).first()
        if user:
            user.nome = form.nome.data
            user.login = form.login.data
            # Apenas atualizar a senha, se for fornecida:
            if form.senha.data:
                user.senha = generate_password_hash(form.senha.data)
            user.email = form.email.data
            user.grupo = form.grupo.data
            user.telefone = form.telefone.data
            user.cargo = form.cargo.data
            user.ativo = form.ativo.data
            user.setor = form.setor.data
            db.session.commit()
            flash("Usuário atualizado com sucesso!", 'sucess')
    return redirect(url_for('users'))


@app.route('/user/desative/<int:id>', methods=['POST'])
def desative_user(id):
    user = User.query.filter_by(id=id).first()
    form = FormUser(request.form)
    if user:
        user.ativo = 'Desativado'
        db.session.commit()
        flash('Usuário desativado com sucesso!')
    else:
        flash('Não foi possível desativa o usuário')
    return redirect(url_for('users'))