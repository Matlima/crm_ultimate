from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Customer
from helpers.forms_helpers import FormCustomer, is_admin
from templates.customers import *
from uploads import *

@app.route('/customers')
def customer():

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('dashboard')))
    adm = is_admin()
    page = request.args.get('page', 1, type=int)
    lista = (
        db.session.query(Customer)
        .order_by(Customer.id)  # Ordena pelo campo 'data' em ordem decrescente
        .paginate(page=page, per_page=10)
    )

    return render_template('customers/customers.html',
                           titulo='Clientes',
                           clientes=lista,
                           is_admin=adm
                           )

@app.route('/customers/new')
def new_customer():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormCustomer()
    return render_template('customers/add_customer.html', titulo='Novo Cliente', form=form)

@app.route('/customers/add', methods=['POST'])
def created_customer():
    form = FormCustomer(request.form)

    # if not form.validate_on_submit():
    #    return redirect(url_for('customer'))

    razao_social = form.razao_social.data
    nome_fantasia = form.nome_fantasia.data
    cpfecnpj = form.cpfecnpj.data
    inscricao_estadual = form.inscricao_estadual.data
    inscricao_municipal = form.inscricao_municipal.data
    telefone = form.telefone.data
    celular = form.celular.data
    email = form.email.data
    tipo_conta = form.tipo_conta.data
    endereco = form.endereco.data
    bairro = form.bairro.data
    cidade = form.cidade.data
    estado = form.estado.data
    numero = form.numero.data
    cep = form.cep.data
    complemento = form.complemento.data

    customer_cpfecnpj = Customer.query.filter_by(cpfecnpj=cpfecnpj).first()

    if customer_cpfecnpj:
        flash('Cliente já existente!')

    novo_customer = Customer(razao_social=razao_social, nome_fantasia=nome_fantasia, cpfecnpj=cpfecnpj, inscricao_estadual=inscricao_estadual,
                             inscricao_municipal=inscricao_municipal, telefone=telefone, celular=celular, email=email, tipo_conta=tipo_conta,
                             endereco=endereco, bairro=bairro, cidade=cidade, estado=estado, numero=numero, cep=cep,complemento=complemento)
    db.session.add(novo_customer)
    db.session.commit()
    flash('Cliente adicionado com sucesso!')
    return redirect(url_for('customer'))


@app.route('/customers/edit/<int:id>')
def edit_customer(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))

    customer = Customer.query.filter_by(id=id).first()

    form = FormCustomer()
    form.razao_social.data = customer.razao_social
    form.nome_fantasia.data = customer.nome_fantasia
    form.cpfecnpj.data = customer.cpfecnpj
    form.inscricao_estadual.data = customer.inscricao_estadual
    form.inscricao_municipal.data = customer.inscricao_municipal
    form.telefone.data = customer.telefone
    form.celular.data = customer.celular
    form.email.data = customer.email
    form.tipo_conta.data = customer.tipo_conta
    form.endereco.data = customer.endereco
    form.bairro.data = customer.bairro
    form.cidade.data = customer.cidade
    form.estado.data = customer.estado
    form.numero.data = customer.numero
    form.cep.data = customer.cep
    form.complemento.data = customer.complemento
    return render_template('customers/edit_customer.html', titulo='Editando Cliente', id=id, form=form)



@app.route('/customers/info/<int:id>')
def info_customer(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))

    customer = Customer.query.filter_by(id=id).first()

    form = FormCustomer()
    form.razao_social.data = customer.razao_social
    form.nome_fantasia.data = customer.nome_fantasia
    form.cpfecnpj.data = customer.cpfecnpj
    form.inscricao_estadual.data = customer.inscricao_estadual
    form.inscricao_municipal.data = customer.inscricao_municipal
    form.telefone.data = customer.telefone
    form.celular.data = customer.celular
    form.email.data = customer.email
    form.tipo_conta.data = customer.tipo_conta
    form.endereco.data = customer.endereco
    form.bairro.data = customer.bairro
    form.cidade.data = customer.cidade
    form.estado.data = customer.estado
    form.numero.data = customer.numero
    form.cep.data = customer.cep
    form.complemento.data = customer.complemento
    return render_template('customers/info_customer.html', titulo='Informações do cliente', id=id, form=form)


@app.route('/customers/update', methods=['POST'])
def update_customer():
    form = FormCustomer(request.form)
    customer = Customer.query.filter_by(id=request.form['id']).first()
    if form.validate_on_submit():
        if customer:
            try:
                customer.razao_social = form.razao_social.data
                customer.nome_fantasia = form.nome_fantasia.data
                customer.cpfecnpj = form.cpfecnpj.data
                customer.inscricao_estadual = form.inscricao_estadual.data
                customer.inscricao_municipal = form.inscricao_municipal.data
                customer.telefone = form.telefone.data
                customer.celular = form.celular.data
                customer.email = form.email.data
                customer.tipo_conta = form.tipo_conta.data
                customer.endereco = form.endereco.data
                customer.bairro = form.bairro.data
                customer.cidade = form.cidade.data
                customer.estado = form.estado.data
                customer.numero = form.numero.data
                customer.cep = form.cep.data
                customer.complemento = form.complemento.data

                db.session.commit()
                flash("Cliente atualizado com sucesso!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Erro ao atualizar o cliente: {str(e)}", "error")
            return redirect(url_for('customer'))
        else:
            flash("Cliente não encontrado", "error")
            return redirect(url_for('edit_customer', id=request.form['id']))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f"Error in {fieldName}: {err}", "error")
        flash("Form validation failed", "error")
    return redirect(url_for('edit_customer', id=request.form['id']))


@app.route('/customers/delete/<int:id>')
def delete_customer(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))

    try:
        Customer.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Cliente excluido com sucesso!')
    except InterruptedError:
        db.session.rollback()
        flash('Erro: Cliente está vinculado a outras atividades. Exclua as atividades relacionadas primeiro.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir cliente: {str(e)}", "error")

    return redirect(url_for('customer'))
