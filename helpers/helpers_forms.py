import os
from application import app
from flask import session
from models.models import User,Customer, Activity
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateTimeField, TextAreaField, validators, BooleanField, DecimalField
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
    cpfecnpj = StringField('CPF/CNPJ')
    cpf = StringField('CPF')
    inscricao_estadual = StringField('Inscrição Estadual')
    inscricao_municipal = StringField('Inscrição Municipal')
    telefone = StringField('Telefone', [validators.Length(min=1, max=50)], render_kw={"placeholder": "Apenas os números"})
    celular = StringField('Celular', [validators.Length(min=1, max=50)], render_kw={"placeholder": "Apenas os números"})
    email = StringField('E-mail', [validators.Length(min=1, max=100)])
    tipo_conta = SelectField('Tipo de Conta', choices=[
        ('Pós-Pago', 'Pós-Pago'),
        ('Pré-Pago', 'Pré-Pago'),])
    endereco = StringField('Endereço', [ validators.Length(min=1, max=100)])
    bairro = StringField('Bairro', [validators.Length(min=1, max=100)])
    cidade = StringField('Cidade', [validators.Length(min=1, max=100)])
    estado = SelectField('Estado', choices=[
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    ], validators=[DataRequired()])
    cep = StringField('CEP', [validators.Length(min=1, max=10)], render_kw={"placeholder": "Apenas os números"})
    numero = StringField('Número', [validators.Length(min=1, max=10)])
    complemento = StringField('Complemento')
    login_gov = StringField('Login', render_kw={"placeholder": "Caso seja o mesmo que o cadastro, pode deixar em branco"})
    senha_gov = PasswordField('Senha', validators=[Optional(), Length(min=0, max=250)])
    check_acessorias = BooleanField('Acessórias')
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


class FormProspect(FlaskForm):
    data_hora_cadastro = DateTimeField('Cadastro', format='%d-%m-%YT%H:%M')
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(min=1, max=100)])
    nome_completo = StringField('Nome', validators=[DataRequired(), Length(min=1, max=100)])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=1, max=100)])
    observacao = TextAreaField('Observação')
    cadastrar = SubmitField('Salvar')

class FormPlano(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=1, max=100)])
    descricao = TextAreaField('Descricao')
    periodicidade = StringField('Periodicidade', validators=[DataRequired(), Length(min=1, max=100)])
    preco = DecimalField('Preço', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo'),])
    cadastrar = SubmitField('Salvar')


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
