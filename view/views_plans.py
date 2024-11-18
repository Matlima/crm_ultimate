from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Plan, CategoryPlan, User
from helpers.forms_helpers import is_admin, FormPlano, FormCategoryPlano
from templates.customers import *
from uploads import *
from datetime import datetime


## Methods Routes:

@app.route('/products')
def plan():
    listPlans = Plan.query.order_by(Plan.id)
    listCategories = CategoryPlan.query.order_by(CategoryPlan.id)
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('dashboard')))
    # adm = is_admin()

    page = request.args.get('page', 1, type=int)
    listPlans = (
        db.session.query(Plan)
        .order_by(Plan.id)  # Ordena pelo campo 'data' em ordem decrescente
        .paginate(page=page, per_page=10)
    )
    listCategories = (
        db.session.query(CategoryPlan)
        .order_by(CategoryPlan.id)  # Ordena pelo campo 'data' em ordem decrescente
        .paginate(page=page, per_page=5)
    )
    return render_template('products/products.html',
                           plans=listPlans,
                           categories=listCategories
                           # is_admin=adm
                           )

@app.route('/products/new')
def new_plan():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormPlano()
    categories = CategoryPlan.query.all()
    return render_template('products/add_plan.html',
                           form=form,
                           categories=categories
                           )

@app.route('/products/add', methods=['POST'])
def created_plan():
    form = FormPlano(request.form)
    nome = form.nome.data
    descricao = form.descricao.data
    periodicidade = form.periodicidade.data
    preco = form.preco.data
    status = form.status.data
    tipo = form.tipo.data
    category = form.id_category.data

    novo_plano = Plan(nome=nome,
                      descricao=descricao,
                      preco=preco,
                      status=status,
                      periodicidade=periodicidade,
                      tipo=tipo,
                      id_category=category
                      )
    db.session.add(novo_plano)
    db.session.commit()
    flash('Plan adicionado com sucesso!')
    return redirect(url_for('plan'))

@app.route('/products/edit/<int:id>')
def edit_plan(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))

    form = FormPlano()
    # Preenche o select de categorias
    form.id_category.choices = [(category.id, category.nome) for category in CategoryPlan.query.all()]

    # Busca o plano específico
    plan = Plan.query.filter_by(id=id).first()

    # Preenche os campos do formulário com os valores do plano
    form.nome.data = plan.nome
    form.status.data = plan.status
    form.descricao.data = plan.descricao
    form.preco.data = plan.preco
    form.periodicidade.data = plan.periodicidade
    form.tipo.data = plan.tipo
    form.id_category.data = plan.id_category  # Categoria selecionada

    return render_template('products/edit_plan.html',
                           id=id,
                           form=form
                           )


# --------------------------------
# Category Plan:

@app.route('/products/category/new')
def new_category_plan():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormCategoryPlano()
    return render_template('products/category_plan/add_category.html',
                           form=form
                           )


@app.route('/products/category/add', methods=['POST'])
def created_category_plan():
    form = FormCategoryPlano(request.form)
    form.id_user.choices = [(usuario.id, usuario.nome) for usuario in User.query.all()]

    nome = form.nome.data
    ativo = form.ativo.data
    user = session["usuario_id"]

    nova_categoria = CategoryPlan(nome=nome, ativo=ativo, id_user=user)
    db.session.add(nova_categoria)
    db.session.commit()

    flash('Categoria adicionada com sucesso!')
    return redirect(url_for('plan'))


@app.route('/products/category/edit/<int:id>')
def edit_category_plan(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))

    category = CategoryPlan.query.filter_by(id=id).first()
    form = FormCategoryPlano()

    # Popula o campo SelectField com as opções de usuários
    form.id_user.choices = [(user.id, user.nome) for user in User.query.all()]

    # Preenche os campos para edição
    form.nome.data = category.nome
    form.ativo.data = category.ativo

    return render_template('products/category_plan/edit_category.html',
                           titulo="Editando categoria",
                           id=id,
                           form=form,
                           usuarios=User.query.all()  # Envia os usuários para o front-end
                           )






## Methods Actions:

@app.route('/products/update', methods=['POST'])
def update_plan():
    form = FormPlano(request.form)

    # Adicionar as opções de categoria dinamicamente
    form.id_category.choices = [(category.id, category.nome) for category in CategoryPlan.query.all()]

    plan = Plan.query.filter_by(id=request.form['id']).first()

    if form.validate_on_submit():
        if plan:
            plan.nome = form.nome.data
            plan.status = form.status.data
            plan.descricao = form.descricao.data
            plan.preco = form.preco.data
            plan.periodicidade = form.periodicidade.data
            plan.tipo = form.tipo.data
            plan.id_category = form.id_category.data
            db.session.commit()
            flash('Plan atualizado com sucesso', 'success')
            return redirect(url_for('plan'))
        else:
            flash('Plano não encontrado', 'error')
            return redirect(url_for('edit_plan', id=request.form['id']))

    # Se houver erros de validação, você pode exibi-los aqui ou redirecionar o usuário
    flash('Erro ao validar o formulário', 'error')
    return redirect(url_for('edit_plan', id=request.form['id']))


@app.route('/products/delete/<int:id>')
def delete_plan(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proximo=url_for('novo')))

    try:
        Plan.query.filter_by(id=id).delete()
        db.session.commit()
        flash("Produto excluida com sucesso!")
    except InterruptedError:
        db.session.rollback()
        flash('Erro: Produto está vinculado a outras(os) proposta/contrato. Exclua as(os) proposta/contrato relacionados primeiro.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir produto: {str(e)}", "error")

    return redirect(url_for('plan'))


# --------------------------------
# Category Plan:
@app.route('/products/category/delete/<int:id>')
def delete_category_plan(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proximo=url_for('novo')))

    try:
        CategoryPlan.query.filter_by(id=id).delete()
        db.session.commit()
        flash("Categoria excluida com sucesso!")
    except InterruptedError:
        db.session.rollback()
        flash('Erro: Categoria está vinculado a outros produto. Exclua os produtos relacionados primeiro.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir categoria: {str(e)}", "error")

    return redirect(url_for('plan'))


@app.route('/products/category/update', methods=['POST'])
def update_category_plan():
    form = FormCategoryPlano(request.form)

    # Popula as opções de id_user novamente ao submeter o formulário
    form.id_user.choices = [(user.id, user.nome) for user in User.query.all()]

    if form.validate_on_submit():
        category = CategoryPlan.query.filter_by(id=request.form['id']).first()
        if category:
            category.nome = form.nome.data
            category.ativo = form.ativo.data
            category.id_user = form.id_user.data  # Atualiza o id_user selecionado
            db.session.commit()
            flash("Categoria atualizada com sucesso!", "success")
    else:
        # Exibe os erros de validação
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Erro no campo {getattr(form, field).label.text}: {error}", "error")

    return redirect(url_for('plan'))