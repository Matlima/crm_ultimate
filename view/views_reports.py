from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from application import app, db
from models.models import User, Activity
from helpers.forms_helpers import FormUser
from flask_bcrypt import generate_password_hash
from sqlalchemy.exc import IntegrityError

@app.route('/reports')
def report():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('dashboard')))

    return render_template('reports/reports.html',
                           titulo='Relatórios'
                           )


@app.route('/report')
def report_user():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('dashboard')))

    return render_template('reports/reports_user.html',
                           titulo='Relatórios'
                           )