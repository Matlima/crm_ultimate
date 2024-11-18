from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Customer, CustomerPortfolio, User, PortfolioItem, Prospect, Activity
from helpers.forms_helpers import FormCustomerPortfolio, is_admin, FormPortfolioItem, FormActivity
from datetime import datetime


# Methods Routes:
@app.route('/my_portfolio')
def my_portfolio_customers_prospect():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('dashboard')))

    adm = is_admin()
    usuario_id = session["usuario_id"]
    user = User.query.get(usuario_id)

    # Pega todos os portfólios onde o usuário logado é o responsável
    portfolio_user = CustomerPortfolio.query.filter_by(responsavel_id=user.id).all()

    # Extrai todos os IDs de portfólio para filtrar os itens
    portfolio_ids = [portfolio.id for portfolio in portfolio_user]

    # Filtra os itens de portfólio onde o portfolio_id está na lista de IDs dos portfólios do usuário
    page = request.args.get('page', 1, type=int)
    itens_carteiras = PortfolioItem.query.filter(PortfolioItem.portfolio_id.in_(portfolio_ids)).paginate(page=page,
                                                                                                         per_page=10)

    return render_template('my_user/my_customers_and_prospects.html',
                           titulo='Minha carteira',
                           itens_carteiras=itens_carteiras,
                           is_admin=adm
                           )


@app.route('/my_portfolio/activities/new/<int:id>/<string:tipo>', methods=['GET', "POST"])
def my_portfolio_new_activity(tipo, id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormActivity()
    usuario_id = session["usuario_id"]
    adm = is_admin()
    # grupo = type_user()

    return render_template('activities/add_activity_my.html',
                           titulo='Nova atividade',
                           form=form,
                           clientes=Customer.query.all(),
                           prospects=Prospect.query.all(),
                           usuarios=User.query.all(),
                           is_admin=adm,
                           id=id,
                           tipo=tipo
                           )

@app.route('/my_portfolio/activities/add', methods=['POST'])
def my_portfolio_add_activity():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))

    usuario_id = session["usuario_id"]

    form = FormActivity(request.form)
    # Obtenha os valores do formulário
    id = request.form.get('id')
    tipo = request.form.get('tipo')


    # Verifica se id está presente e é válido
    if id and id.isdigit():
        id = int(id)  # Converte para inteiro se válido
    else:
        flash('ID inválido ou não fornecido.', 'error')
        return redirect(url_for('my_portfolio_customers_prospect'))


    # Obtém os demais dados do formulário
    status = form.status.data
    titulo = form.titulo.data
    descricao = form.descricao.data
    tipo2 = form.tipo.data

    # Verifica o tipo e cria a atividade correspondente
    if tipo == 'cliente':
        new_activity = Activity(
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            titulo=titulo,
            descricao=descricao,
            tipo=tipo2,
            status=status,
            cliente_id=id,
            usuario_id=usuario_id
        )
    elif tipo == 'prospect':
        new_activity = Activity(
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            titulo=titulo,
            descricao=descricao,
            tipo=tipo2,
            status=status,
            prospect_id=id,
            usuario_id=usuario_id
        )
    else:
        flash('Tipo inválido!', 'error')
        return redirect(url_for('my_portfolio_customers_prospect'))

    # Salva a nova atividade no banco de dados
    db.session.add(new_activity)
    db.session.commit()

    flash('Atividade adicionada com sucesso!')
    return redirect(url_for('my_portfolio_customers_prospect'))
