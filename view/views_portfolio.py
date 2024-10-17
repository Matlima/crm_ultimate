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


@app.route('/portfolio/config/<int:id>', methods=['GET', 'POST'])
def config_portfolio(id):
    page = request.args.get('page', 1, type=int)
    itens_carteiras = PortfolioItem.query.filter_by(portfolio_id=id).paginate(page=page, per_page=10)
    formItem = FormPortfolioItem()

    # Buscar o portfólio atual
    portfolio = CustomerPortfolio.query.get(id)

    # Instanciar o formulário com request.form para suporte ao POST
    form = FormCustomerPortfolio(request.form or None)

    # Definir as choices para os campos 'usuario_id' e 'responsavel_id'
    usuarios = [(usuario.id, usuario.nome) for usuario in User.query.all()]
    form.usuario_id.choices = [(0, "Selecione um usuário")] + usuarios
    form.responsavel_id.choices = [(0, "Selecione um responsável")] + usuarios

    # Processar a submissão do formulário no POST
    if request.method == 'POST' and form.validate_on_submit():
        portfolio.nome = form.nome.data
        portfolio.ativo = form.ativo.data
        portfolio.responsavel_id = form.responsavel_id.data
        portfolio.usuario_id = form.usuario_id.data

        # Tratar o campo data_validade corretamente como datetime
        portfolio.data_validade = form.data_validade.data

        portfolio.observacao = form.observacao.data

        # Commit das alterações no banco de dados
        db.session.commit()
        flash("Carteira de cliente atualizada com sucesso!")
        return redirect(url_for('config_portfolio', id=id))

    # Pré-preencher o formulário no GET
    if request.method == 'GET':
        form.nome.data = portfolio.nome
        form.ativo.data = portfolio.ativo
        form.responsavel_id.data = portfolio.responsavel_id
        form.usuario_id.data = portfolio.usuario_id

        # Preencher corretamente o campo data_validade como datetime
        # if portfolio.data_validade:
            # form.data_validade.data = portfolio.data_validade
        # else:
            #form.data_validade.data = datetime.now()  # Caso não haja valor, preencher com data atual

        form.observacao.data = portfolio.observacao

    return render_template('customers/portfolio/config_portfolio.html',
                           form=form,
                           formItem=formItem,
                           itens_carteiras=itens_carteiras,
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
    # data_validade = form.data_validade.data
    observacao = form.observacao.data

    new_portfolio = CustomerPortfolio(
        data_criacao=data_criacao,
        usuario_id=usuario,
        responsavel_id=responsavel,
        nome=nome,
        ativo=ativo,
        # data_validade=data_validade,
        observacao=observacao
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


@app.route('/portfolio/ativate/<int:id>')
def ativar_portfolio(id):
    usuario_id = session['usuario_id']
    usuario = User.query.filter_by(id=usuario_id).first()
    portfolio = CustomerPortfolio.query.filter_by(id=id).first()

    if usuario.grupo == 'Administrador':
        portfolio.ativo = True
        db.session.commit()
        flash('Carteira de clientes ativada com sucesso!')
    else:
        flash('O usuário logado não tem autorização para ativar a carteira, apenas administradores.')

    return redirect(url_for('portfolio'))


@app.route('/portfolio/<int:id>/edit', methods=['GET', 'POST'])
def edit_portfolio(id):
    # Buscar o portfólio que será editado
    portfolio = CustomerPortfolio.query.get_or_404(id)

    # Obter a página atual da paginação
    page = request.args.get('page', 1, type=int)
    itens_carteiras = PortfolioItem.query.filter_by(portfolio_id=id).paginate(page=page, per_page=10)
    formItem = FormPortfolioItem()

    # Instanciar o formulário com request.form
    form = FormCustomerPortfolio(request.form or None)

    # Definir as choices para os campos 'usuario_id' e 'responsavel_id'
    usuarios = [(usuario.id, usuario.nome) for usuario in User.query.all()]
    form.responsavel_id.choices = usuarios

    if request.method == 'POST':
        print("Valores enviados no formulário:")
        print(request.form)  # Isso imprime os valores enviados pelo formulário

        if form.validate_on_submit():
            # Atualizar os dados do portfólio
            portfolio.nome = form.nome.data
            portfolio.ativo = form.ativo.data
            portfolio.responsavel_id = form.responsavel_id.data
            # portfolio.data_validade = form.data_validade.data
            portfolio.observacao = form.observacao.data

            # Commit ao banco de dados
            db.session.commit()
            flash("Carteira de cliente atualizada com sucesso!")
            return redirect(url_for('portfolio'))
        else:
            print("Erros de validação: ", form.errors)
            flash("Erro ao atualizar a carteira", "danger")

    # Pré-preencher os campos do formulário no GET
    if request.method == 'GET':
        form.nome.data = portfolio.nome
        form.ativo.data = portfolio.ativo
        form.responsavel_id.data = portfolio.responsavel_id
        # if portfolio.data_validade:
            # form.data_validade.data = portfolio.data_validade.strftime('%Y-%m-%dT%H:%M')  # Formato datetime-local
        form.observacao.data = portfolio.observacao

    return render_template('customers/portfolio/config_portfolio.html',
                           titulo='Editar Carteira',
                           form=form,
                           formItem=formItem,
                           itens_carteiras=itens_carteiras,
                           portfolio=portfolio,
                           id=id)






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

@app.route('/portfolio/<int:id>/item/transfer/<int:item_id>', methods=['POST'])
def transferir_unico_item_portfolio(id, item_id):
    # Obter o portfolio de destino do form
    portfolioTransfer = request.form.get('carteira')

    # Busca o item específico do portfolio atual
    itemPortfolio = PortfolioItem.query.filter_by(id=item_id, portfolio_id=id).first()

    # Verifica se o item existe e se foi selecionada uma nova carteira
    if itemPortfolio and portfolioTransfer:
        itemPortfolio.portfolio_id = portfolioTransfer  # Atualiza o portfolio_id do item

        db.session.commit()  # Realiza o commit após a transferência do item
        flash('Cliente/Prospect transferido com sucesso!', 'success')
    else:
        flash('Não foi possível transferir o item.', 'danger')

    # Redireciona para a página de configuração do portfólio
    return redirect(url_for('config_portfolio', id=id))

@app.route('/portfolio/<int:id>/item/transfer-all', methods=['POST'])
def transferir_todos_item_portfolio(id):
    # Obter o portfolio de destino do form
    portfolioTransfer = request.form.get('carteira')

    # Busca todos os itens do portfolio atual
    itemsPortfolio = PortfolioItem.query.filter_by(portfolio_id=id).all()

    # Verifica se há itens a transferir
    if itemsPortfolio and portfolioTransfer:
        for item in itemsPortfolio:
            item.portfolio_id = portfolioTransfer  # Atualiza o portfolio_id de cada item

        db.session.commit()  # Realiza o commit após a transferência de todos os itens
        flash('Todos os clientes/prospect foram transferidos com sucesso!', 'success')
    else:
        flash('Não foi possível transferir os itens.', 'danger')

    # Redireciona para a página de configuração do portfólio
    return redirect(url_for('config_portfolio', id=id))

















