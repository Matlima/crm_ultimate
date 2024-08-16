import os
from application import app
from flask import session
from models.models import User,Customer, Activity
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateTimeField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Length


class FormularioJogo(FlaskForm):
    nome = StringField('Nome do jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')


class FormUser(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=1, max=300)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(min=1, max=100)])
    senha = PasswordField('Senha', validators=[Optional(), Length(min=1, max=100)])
    login = StringField('Login', validators=[DataRequired(), Length(min=1, max=100)])
    grupo = SelectField('Grupo de Usuário', choices=[('funcionario', 'Funcionário'), ('diretoria', 'Diretoria'),
                                                     ('administrador', 'Administrador')])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=1, max=30)])
    ativo = SelectField('Ativo', choices=[('Ativo', 'Ativo'), ('Desativado', 'Desativado')])
    cargo = StringField('Cargo', validators=[DataRequired(), Length(min=1, max=50)])
    setor = StringField('Setor', validators=[DataRequired(), Length(min=1, max=50)])
    registrar = SubmitField('Salvar')
    entrar = SubmitField('Login')

class FormCustomer(FlaskForm):
    razao_social = StringField('Razão Social', [validators.DataRequired(), validators.Length(min=1, max=200)])
    nome_fantasia = StringField('Nome Fantasia', [validators.DataRequired(), validators.Length(min=1, max=100)])
    cnpj = StringField('CNPJ', [validators.Length(min=1, max=30)])
    cpf = StringField('CPF', [validators.Length(min=1, max=30)])
    inscricao_estadual = StringField('Inscrição Estadual', [validators.Length(min=1, max=50)])
    inscricao_municipal = StringField('Inscrição Municipal', [validators.Length(min=1, max=50)])
    telefone = StringField('Telefone', [validators.Length(min=1, max=50)])
    celular = StringField('Celular', [validators.Length(min=1, max=50)])
    email = StringField('E-mail', [validators.Length(min=1, max=100)])
    tipo_conta = SelectField('Tipo de Conta', choices=[('Pré-Pago', 'Pré-Pago'), ('Pós-Pago', 'Pós-Pago'),])
    endereco = StringField('Endereço', [ validators.Length(min=1, max=100)])
    bairro = StringField('Bairro', [validators.Length(min=1, max=100)])
    cidade = StringField('Cidade', [validators.Length(min=1, max=100)])
    estado = StringField('Estado', [validators.Length(min=1, max=5)])
    cep = StringField('CEP', [validators.Length(min=1, max=10)])
    numero = StringField('Número', [validators.Length(min=1, max=10)])
    complemento = StringField('Complemento', [validators.Length(min=1, max=100)])
    cadastrar = SubmitField('Salvar')


class FormActivity(FlaskForm):
    data_inicio = DateTimeField('Data Início', [DataRequired()], format='%Y-%m-%dT%H:%M')
    data_fim = DateTimeField('Data Fim', format='%Y-%m-%dT%H:%M')
    cliente_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    usuario_id = SelectField('Usuário', coerce=int, validators=[DataRequired()])
    titulo = StringField('Título', validators=[DataRequired(), Length(min=1, max=100)])
    descricao = TextAreaField('Descrição')
    status = SelectField('Status', choices=[('Pendente', 'Pendente'), ('Em andamento', 'Em andamento'), ('Concluído', 'Concluído'),])
    tipo = SelectField('Status', choices=[('Atividade', 'Atividade'), ('Relatório', 'Relatório'), ('Solicitação', 'Solicitação'),])
    salvar = SubmitField('Salvar')
    concluir = SubmitField('Concluir')



# Funções para upload de imagem na pasta /Upload
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH']), arquivo)

def is_admin():
    id = session["usuario_id"]
    usuario = User.query.filter_by(id=id).first()
    if usuario.grupo == 'administrador':
        return True
    else:
        return False
