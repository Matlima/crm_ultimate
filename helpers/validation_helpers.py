import os
from application import app
from flask import session
from models.models import User,Customer, Activity
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateTimeField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Length


def is_admin():
    id = session["usuario_id"]
    usuario = User.query.filter_by(id=id).first()
    if usuario.grupo == 'Administrador':
        return True
    else:
        return False

def is_cliente():
    id=session["usuario_id"]
    usuario = User.query.filter_by(id=id).first()
    if usuario.grupo == 'cliente':
        return True
    else:
        return False

def type_user():
    id = session["usuario_id"]
    usuario = User.query.filter_by(id=id).first()
    return usuario.grupo