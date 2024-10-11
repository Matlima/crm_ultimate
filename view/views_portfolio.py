from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Customer, CustomerPortfolio, User
from helpers.forms_helpers import FormCustomerPortfolio, is_admin
from templates.customers import *
from uploads import *


# Methods Routes:

@app.route('/portfolio')
def portfolio():

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('dashboard')))
    adm = is_admin()

    page = request.args.get('page', 1, type=int)

    lista = (
        db.session.query(CustomerPortfolio)
        .order_by(CustomerPortfolio.id)  # Ordena pelo campo 'data' em ordem decrescente
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




# Methods Action:


