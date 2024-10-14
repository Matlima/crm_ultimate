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
    # Paginação dos itens de carteiras filtrados pelo 'CustomerPortfolio' específico
    itens_carteiras = PortfolioItem.query.filter_by(portfolio_id=id).paginate(page=page, per_page=10)
    portfolio = CustomerPortfolio.query.filter_by(id=id).first()

    form = FormCustomerPortfolio()

    formItem = FormPortfolioItem()

    # Populando as opções dos selects
    clientes = Customer.query.all()  # Lista de clientes
    prospects = Prospect.query.all()  # Lista de prospects
    usuarios = User.query.all()  # Lista de usuários
    portfolios = CustomerPortfolio.query.all()  # Lista de portfolios

    # Assegura que sempre haverá uma lista, mesmo que vazia
    formItem.cliente.choices = [(cliente.id, cliente.razao_social) for cliente in clientes] or []
    formItem.prospect.choices = [(prospect.id, prospect.nome_completo) for prospect in prospects] or []
    formItem.usuario.choices = [(usuario.id, usuario.nome) for usuario in usuarios] or []
    formItem.portfolio.choices = [(portfolio.id, portfolio.nome) for portfolio in portfolios] or []

    form.nome.data = portfolio.nome
    form.ativo.data = portfolio.ativo
    form.responsavel_id.data = portfolio.responsavel_id

    adm = is_admin()

    # Renderizar a página com os dados de portfolio_item
    return render_template('customers/portfolio/config_portfolio.html',
                           itens_carteiras=itens_carteiras,
                           form=form,
                           formItem=formItem,
                           is_admin=adm,
                           carteiras=CustomerPortfolio.query.all(),
                           clientes=Customer.query.all(),
                           prospects=Prospect.query.all(),
                           usuarios=User.query.all(),
                           id=id
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
@app.route('/portfolio/<int:id>/item/add', methods=['GET', 'POST'])
def created_item_portfolio(id):
    form = FormPortfolioItem(request.form)

    # Populando as opções dos selects
    clientes = Customer.query.all()  # Lista de clientes
    prospects = Prospect.query.all()  # Lista de prospects
    usuarios = User.query.all()  # Lista de usuários
    portfolios = CustomerPortfolio.query.all()  # Lista de portfolios

    # Assegura que sempre haverá uma lista, mesmo que vazia
    form.cliente.choices = [(cliente.id, cliente.razao_social) for cliente in clientes] or []
    form.prospect.choices = [(prospect.id, prospect.nome_completo) for prospect in prospects] or []
    form.usuario.choices = [(usuario.id, usuario.nome) for usuario in usuarios] or []
    form.portfolio.choices = [(portfolio.id, portfolio.nome) for portfolio in portfolios] or []

    if form.validate_on_submit():  # Verifica se o formulário foi submetido corretamente
        cliente = form.cliente.data  # O valor do cliente selecionado
        prospect = form.prospect.data  # O valor do prospect selecionado
        usuario = form.usuario.data  # O valor do usuário selecionado
        portfolio = form.portfolio.data  # O valor do portfólio selecionado

        # Criar o novo item no portfólio
        new_item = PortfolioItem(
            cliente_id=cliente if cliente else None,  # Apenas define se cliente for selecionado
            prospect_id=prospect if prospect else None,  # Apenas define se prospect for selecionado
            portfolio_id=portfolio,  # Este é o id do portfólio que vem da URL
            usuario_id=usuario  # Usuário da sessão
        )

        # Adiciona e comita no banco
        db.session.add(new_item)
        db.session.commit()

        flash("Item adicionado na carteira de cliente com sucesso!")
        return redirect(url_for('config_portfolio', id=id))  # Redireciona para a página de configuração do portfólio
    else:
        # Exibe os erros de validação no console ou log do servidor
        print("Erros de validação do formulário:", form.errors)
        flash(f"Erro ao adicionar o item ao portfólio: {form.errors}", "danger")

    return render_template('customers/portfolio/config_portfolio.html', form=form, id=id)
