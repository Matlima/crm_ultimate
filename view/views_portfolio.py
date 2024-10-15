from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Customer, CustomerPortfolio, User, PortfolioItem, Prospect
from helpers.forms_helpers import FormCustomerPortfolio, is_admin, FormPortfolioItem
from datetime import datetime


# Methods Routes:
@app.route('/portfolios')
def portfolio():

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('dashboard')))
    adm = is_admin()

    page = request.args.get('page', 1, type=int)

    # Especificando a junção correta para as duas FK: usuario_id e responsavel_id
    lista = (
        db.session.query(CustomerPortfolio)
        # .join(User, CustomerPortfolio.usuario_id == User.id)  # Junção com o criador da carteira
        .join(User, CustomerPortfolio.responsavel_id == User.id)  # Junção com o responsável pela carteira
        .order_by(CustomerPortfolio.id)
        .paginate(page=page, per_page=10)
    )

    return render_template('customers/portfolio/list_portfolio.html',
                           titulo='Carteira de clientes',
                           carteiras=lista,
                           is_admin=adm
                           )


@app.route('/portfolio/new')
def new_portfolio():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))

    form = FormCustomerPortfolio()
    usuarios = [(usuario.id, usuario.nome) for usuario in User.query.all()]
    form.responsavel_id.choices = usuarios

    return render_template('customers/portfolio/add_portfolio.html',
                           titulo='Nova Carteira',
                           form=form,
                           usuarios=User.query.all()
                           )
@app.route('/portfolio/config/<int:id>', methods=['GET'])
def config_portfolio(id):
    page = request.args.get('page', 1, type=int)
    itens_carteiras = PortfolioItem.query.filter_by(portfolio_id=id).paginate(page=page, per_page=10)
    portfolio = CustomerPortfolio.query.get(id)

    form = FormCustomerPortfolio()
    formItem = FormPortfolioItem()

    # Populando as opções dos selects
    clientes = Customer.query.all()
    prospects = Prospect.query.all()
    usuarios = User.query.all()

    # Assegura que os choices estão sempre preenchidos
    formItem.cliente.choices = [("", "Selecione um cliente")] + [(cliente.id, cliente.razao_social) for cliente in clientes]
    formItem.prospect.choices = [("", "Selecione um prospect")] + [(prospect.id, prospect.nome_completo) for prospect in prospects]

    # Preencher usuário e carteira, mas usando readonly ao invés de disabled
    formItem.usuario.choices = [(usuario.id, usuario.nome) for usuario in usuarios]
    usuario_atual_id = session.get("usuario_id")
    formItem.usuario.data = usuario_atual_id
    formItem.usuario.render_kw = {'readonly': True}  # Deixar apenas leitura, não desabilitado

    formItem.portfolio.choices = [(portfolio.id, portfolio.nome)]
    formItem.portfolio.data = portfolio.id
    formItem.portfolio.render_kw = {'readonly': True}  # Deixar apenas leitura, não desabilitado

    form.nome.data = portfolio.nome
    form.ativo.data = portfolio.ativo
    form.responsavel_id.data = portfolio.responsavel_id

    adm = is_admin()

    return render_template('customers/portfolio/config_portfolio.html',
                           form=form,
                           formItem=formItem,
                           is_admin=adm,
                           itens_carteiras=itens_carteiras,
                           carteiras=CustomerPortfolio.query.all(),
                           clientes=Customer.query.all(),
                           prospects=Prospect.query.all(),
                           usuarios=User.query.all(),
                           id=id)



# Methods Action:


@app.route('/portfolio/add', methods=['GET', 'POST'])
def created_portfolio():
    form = FormCustomerPortfolio(request.form)

    form.responsavel_id.choices = [(usuario.id, usuario.nome) for usuario in User.query.all()]
    form.responsavel_id.choices = [(usuario.id, usuario.nome) for usuario in User.query.all()]

    data_criacao = datetime.now()
    ativo = form.ativo.data
    nome = form.nome.data
    responsavel = form.responsavel_id.data
    usuario = session["usuario_id"]

    new_portfolio = CustomerPortfolio(
        data_criacao=data_criacao,
        usuario_id=usuario,
        responsavel_id=responsavel,
        nome=nome,
        ativo=ativo
    )
    db.session.add(new_portfolio)
    db.session.commit()

    flash("Carteira de cliente criado com sucesso!")
    return redirect(url_for('portfolio'))


@app.route('/portfolio/delete/<int:id>')
def delete_portfolio(id):
    usuario_id = session['usuario_id']
    usuario = User.query.filter_by(id=usuario_id).first()
    portfolio = CustomerPortfolio.query.filter_by(id=id).first()

    if usuario.grupo == 'administrador':
        CustomerPortfolio.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Carteira de clientes excluida com sucesso!')
    else:
        flash('O usuário logado não tem autorização para excluir a carteira, apenas administradores.')
    return redirect(url_for('portfolio'))



@app.route('/portfolio/desativate/<int:id>')
def desativar_portfolio(id):
    usuario_id = session['usuario_id']
    usuario = User.query.filter_by(id=usuario_id).first()
    portfolio = CustomerPortfolio.query.filter_by(id=id).first()

    """ QUANDO TIVER PASSANDO O GRUPO DO USUARIO, USAR
    if usuario.grupo == 'administrador':
        portfolio.ativo = False
        db.session.commit()
        flash('Carteira de clientes desativada com sucesso!')
    else:
        flash('O usuário logado não tem autorização para desativar a carteira, apenas administradores.')
    """

    portfolio.ativo = False
    db.session.commit()
    flash('Carteira de clientes desativada com sucesso!')

    return redirect(url_for('portfolio'))


# Item de carteira:

@app.route('/portfolio/<int:id>/item/add', methods=['GET', 'POST'])
def created_item_portfolio(id):
    formItem = FormPortfolioItem(request.form)

    # Populando as opções dos selects antes da validação
    clientes = Customer.query.all()
    prospects = Prospect.query.all()
    usuarios = User.query.all()
    portfolio = CustomerPortfolio.query.get(id)

    # Assegura que os choices estão sempre preenchidos
    formItem.cliente.choices = [("", "Selecione um cliente")] + [(cliente.id, cliente.razao_social) for cliente in clientes]
    formItem.prospect.choices = [("", "Selecione um prospect")] + [(prospect.id, prospect.nome_completo) for prospect in prospects]
    formItem.usuario.choices = [(usuario.id, usuario.nome) for usuario in usuarios]
    formItem.portfolio.choices = [(portfolio.id, portfolio.nome)]

    if formItem.validate_on_submit():
        cliente = formItem.cliente.data
        prospect = formItem.prospect.data
        usuario = formItem.usuario.data
        portfolio = formItem.portfolio.data

        # Criar o novo item no portfólio
        new_item = PortfolioItem(
            cliente_id=cliente if cliente else None,
            prospect_id=prospect if prospect else None,
            portfolio_id=portfolio,
            usuario_id=usuario
        )

        db.session.add(new_item)
        db.session.commit()

        flash("Item adicionado na carteira de cliente com sucesso!")
        return redirect(url_for('config_portfolio', id=id))
    else:
        print("Erros de validação do formulário:", formItem.errors)
        flash(f"Erro ao adicionar o item ao portfólio: {formItem.errors}", "danger")

    form = FormCustomerPortfolio()
    adm = is_admin()
    page = request.args.get('page', 1, type=int)
    itens_carteiras = PortfolioItem.query.filter_by(portfolio_id=id).paginate(page=page, per_page=10)

    return render_template('customers/portfolio/config_portfolio.html',
                           form=form,
                           formItem=formItem,
                           id=id,
                           itens_carteiras=itens_carteiras,
                           carteiras=CustomerPortfolio.query.all(),
                           clientes=Customer.query.all(),
                           prospects=Prospect.query.all(),
                           usuarios=User.query.all())


@app.route('/portfolio/<int:id>/item/delete')
def delete_item_portfolio(id):
    usuario = session['usuario_id']
    usuario = User.query.filter_by(id=usuario).first()
    if usuario.grupo == 'Administrador':
        PortfolioItem.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Item excluido com sucesso')
    else:
        flash('Somente administradores pode excluir o item da carteira.')
    return redirect(url_for('portfolio'))






