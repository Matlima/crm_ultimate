from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Customer
from helpers.helpers_forms import FormCustomer, is_admin
from templates.customers import *
from uploads import *

@app.route('/prospect')
def prospect():
    lista = Customer.query.order_by(Customer.id)
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('dashboard')))
    adm = is_admin()
    return render_template('customers/customers.html', titulo='Clientes', clientes=lista, is_admin=adm)

@app.route('/prospect/new')
def new_prospect():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormCustomer()
    return render_template('prospects/add_prospect.html', form=form)
