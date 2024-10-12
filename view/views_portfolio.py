from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Customer, CustomerPortfolio, User, PortfolioItem, Prospect
from helpers.forms_helpers import FormCustomerPortfolio, is_admin, FormPortfolioItem
from datetime import datetime


# Methods Routes:
@app.route('/portfolio')
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
    portfolio_id = request.args.get('id', type=int)
    print(portfolio_id)

    page = request.args.get('page', 1, type=int)
    # Paginação dos itens de carteiras filtrados pelo 'CustomerPortfolio' específico
    itens_carteiras = PortfolioItem.query.filter_by(portfolio_id=id).paginate(page=page, per_page=10)

    portfolio = CustomerPortfolio.query.filter_by(id=id).first()
    form = FormCustomerPortfolio()

    form.nome.data = portfolio.nome
    form.ativo.data = portfolio.ativo

    form.responsavel_id.data = portfolio.responsavel_id



    # Renderizar a página com os dados de portfolio_item
    return render_template('customers/portfolio/config_portfolio.html',
                           itens_carteiras=itens_carteiras
                           )


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




@app.route('/portfolio/<int:id>/item/add', methods=['GET', 'POST'])
def created_item_portfolio(id):
    form = FormPortfolioItem(request.form)

    form.cliente.choices = [(cliente.id, cliente.razao_social) for cliente in Customer.query.all()]
    form.prospect.choices = [(prospect.id, prospect.nome) for prospect in Prospect.query.all()]

    cliente = form.cliente.data
    prospect = form.cliente.data
    portfolio = id
    usuario = session["usuario_id"]

    new_item = PortfolioItem(
        cliente=cliente,
        prospect=prospect,
        portfolio=portfolio,
        usuario=usuario
    )
    db.session.add(new_item)
    db.session.commit()

    flash("Item adicionado na carteira de cliente com sucesso!")
    return redirect(url_for('portfolio'))






