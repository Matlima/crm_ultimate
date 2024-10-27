import os
from application import app
from flask import session
from models.models import User,Customer, Activity
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateTimeField, TextAreaField, validators, BooleanField, DecimalField, DateField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Length, NumberRange

estados = [
    ('', 'Estado'),
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
]



grupoUsuarios = [
    ('Administrador', 'Administrador'),
    ('Cliente', 'Cliente'),
    ('Diretoria', 'Diretoria'),
    ('Funcionario', 'Funcionário'),
    ('Gerente', 'Gerente')

]

condicoesPagamento = [
    ('A vista', 'A vista'),
    ('Cartão de credito', 'Cartão de credito'),
    ('Cartão de debito', 'Cartão de debito'),
    ('Boleto', 'Boleto'),
    ('Pix', 'Pix')

]


class FormUser(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=1, max=300)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(min=1, max=100)])
    senha = PasswordField('Senha', validators=[Optional(), Length(min=1, max=100)])
    login = StringField('Login', validators=[DataRequired(), Length(min=1, max=100)])
    grupo = SelectField('Grupo de Usuário', choices=[('Funcionario', 'Funcionário'), ('Diretoria', 'Diretoria'),
                                                     ('Administrador', 'Administrador')])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=1, max=30)])
    ativo = SelectField('Ativo', choices=[('Ativo', 'Ativo'), ('Desativado', 'Desativado')])
    cargo = StringField('Cargo', validators=[DataRequired(), Length(min=1, max=50)])
    setor = StringField('Setor', validators=[DataRequired(), Length(min=1, max=50)])
    registrar = SubmitField('Salvar')
    entrar = SubmitField('Login')


class FormCustomerPortfolio(FlaskForm):
    usuario_id = SelectField('Usuário', coerce=int)
    responsavel_id = SelectField('Responsável', coerce=int)
    nome = StringField('Nome', validators=[Length(min=1, max=200)])
    ativo = BooleanField('Ativo')
    # Usando DateTimeField para lidar com datetime, mas com render_kw para mostrar apenas o datepicker
    # data_validade = DateTimeField('Validade', format='%Y-%m-%d %H:%M:%S', render_kw={'type': 'datetime-local'})
    observacao = TextAreaField('Observação')
    salvar = SubmitField('Salvar')


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


class FormPortfolioItem(FlaskForm):
    usuario = SelectField('Usuário', coerce=int,  choices=[])
    portfolio = SelectField('Carteira de cliente', coerce=int, choices=[])

    # Tratar valores vazios como None
    cliente = SelectField('Cliente', coerce=lambda x: int(x) if x else None, choices=[])
    prospect = SelectField('Prospect', coerce=lambda x: int(x) if x else None, choices=[])

    adicionar = SubmitField('Adicionar')

class FormActivity(FlaskForm):
    data_inicio = DateTimeField('Data Início', [DataRequired()], format='%Y-%m-%dT%H:%M')
    data_fim = DateTimeField('Data Fim', format='%Y-%m-%dT%H:%M')
    cliente_id = SelectField('Cliente', coerce=int)
    prospect_id = SelectField('Prospect', coerce=int)
    usuario_id = SelectField('Usuário', coerce=int, validators=[DataRequired()])
    titulo = StringField('Título', validators=[DataRequired(), Length(min=1, max=100)])
    descricao = TextAreaField('Descrição')
    status = SelectField('Status', choices=[('Pendente', 'Pendente'), ('Em andamento', 'Em andamento'), ('Concluído', 'Concluído'),])
    tipo = SelectField('Tipo', choices=[('Atividade', 'Atividade'), ('Visita', 'Visita'), ('Relatório', 'Relatório'),  ('Solicitação', 'Solicitação'),])
    salvar = SubmitField('Salvar')
    concluir = SubmitField('Concluir')


class FormProspect(FlaskForm):
    data_hora_cadastro = DateTimeField('Cadastro', format='%d-%m-%YT%H:%M')
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(min=1, max=100)])
    nome_completo = StringField('Nome', validators=[DataRequired(), Length(min=1, max=100)])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=1, max=100)], render_kw={"placeholder": "+55(71)99999-9999"})
    observacao = TextAreaField('Observação')
    cadastrar = SubmitField('Salvar')

class FormPlano(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=1, max=100)])
    descricao = TextAreaField('Descricao')
    periodicidade = SelectField('Status', choices=[('Único', 'Único'),('Diário', 'Diário'), ('Mensal', 'Mensal'),('Anual', 'Anual'),])
    preco = DecimalField('Preço', validators=[DataRequired()], render_kw={"placeholder": "R$"})
    status = SelectField('Status', choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo'),])
    tipo = SelectField('Tipo', choices=[('Produto', 'Produto'), ('Plano', 'Plano'), ('Serviço', 'Serviço'),])
    id_category = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    cadastrar = SubmitField('Salvar')

class FormCategoryPlano(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=1, max=100)])
    ativo = BooleanField('Ativo')
    id_user = SelectField('Usuário', coerce=int, validators=[DataRequired()])
    cadastrar = SubmitField('Salvar')


class FormProposal(FlaskForm):
    customer_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    responsavel_id = SelectField('Responsável', coerce=int, validators=[DataRequired()])
    nome = StringField('Nome da Proposta', validators=[DataRequired(), Length(min=1, max=300)])
    valor_total = DecimalField('Valor Total', places=2, validators=[DataRequired(), NumberRange(min=0)])
    valor_total_service = DecimalField('Valor Total de Serviços', places=2,
                                       validators=[DataRequired(), NumberRange(min=0)])
    valor_total_plan = DecimalField('Valor Total do Plano', places=2, validators=[DataRequired(), NumberRange(min=0)])
    valor_total_product = DecimalField('Valor Total de Produtos', places=2,
                                       validators=[DataRequired(), NumberRange(min=0)])

    # Ajustando a validação do campo status para garantir que seja obrigatório
    status = SelectField('Status',
                         choices=[('Pendente', 'Pendente'), ('Aprovada', 'Aprovada'), ('Reprovada', 'Reprovada')],
                         validators=[DataRequired()])

    condicoes_pagamento = SelectField('Condições de Pagamento', choices=condicoesPagamento, validators=[DataRequired()])
    condicoes_comerciais = TextAreaField('Condições Comerciais')
    disposicao_gerais = TextAreaField('Disposições Gerais')

    salvar = SubmitField('Salvar')


class FormItemProposta(FlaskForm):
    # proposta_id = SelectField('Proposta', coerce=int)
    plan_id = SelectField('Plano', coerce=int, validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    desconto = FloatField('Desconto (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    total = FloatField('Total', validators=[DataRequired(), NumberRange(min=0)])

    salvar = SubmitField('Salvar')

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
    return usuario.grupo

"""    if usuario.grupo == 'Administrador':
        return True
    else:
        return False
"""