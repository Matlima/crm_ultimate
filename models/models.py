from application import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy import DECIMAL


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), nullable=False)
    grupo = db.Column(db.String(30), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
    cargo = db.Column(db.String(50))
    setor = db.Column(db.String(50))
    ativo = db.Column(db.String(20))
    activities = db.relationship('Activity', backref='usuario', lazy=True)

    def __repr__(self):
        return '<name %r' % self.__name__

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(Integer, primary_key=True, unique=True)
    razao_social = db.Column(String(200), nullable=False)
    nome_fantasia = db.Column(String(200), nullable=False)
    cpfecnpj = db.Column(String(30))
    inscricao_estadual = db.Column(String(50))
    inscricao_municipal = db.Column(String(50))
    telefone = db.Column(String(50))
    celular = db.Column(String(50))
    email = db.Column(String(100))
    tipo_conta = db.Column(String(20))
    endereco = db.Column(String(100))
    bairro = db.Column(String(100))
    cidade = db.Column(String(100))
    estado = db.Column(String(5))
    numero = db.Column(String(10))
    cep = db.Column(String(10))
    complemento = db.Column(String(100))

    # Relacionamento correto com Activity
    activities = db.relationship('Activity', backref='customer')

    def __repr__(self):
        return '<Customer %r>' % self.nome_fantasia

class CustomerPortfolio(db.Model):
    __tablename__ = 'customer_portfolio'
    id = db.Column(Integer, primary_key=True)
    usuario_id = db.Column(Integer, ForeignKey('user.id'), nullable=False)
    responsavel_id = db.Column(Integer, ForeignKey('user.id'), nullable=False)
    data_criacao = db.Column(DateTime, default=datetime.now)
    data_fim = db.Column(DateTime)
    nome = db.Column(String(200))
    ativo = db.Column(db.Boolean)

    def __repr__(self):
        return '<name %r' % self.__name__



class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(Integer, primary_key=True)
    cliente_id = db.Column(Integer, ForeignKey('customer.id'), nullable=False)
    prospect_id = db.Column(Integer, ForeignKey('prospect.id'), nullable=False)
    usuario_id = db.Column(Integer, ForeignKey('user.id'), nullable=False)
    data_inicio = db.Column(DateTime, default=datetime.now)
    data_fim = db.Column(DateTime)
    tipo = db.Column(String(100))
    titulo = db.Column(String(100))
    descricao = db.Column(db.Text)
    status = db.Column(String(20))

    def __repr__(self):
        return '<name %r' % self.__name__


class Prospect(db.Model):
    __tablename__ = 'prospect'
    id = db.Column(db.Integer, primary_key=True)
    data_hora_cadastro = db.Column(db.DateTime, default=datetime.now)
    email = db.Column(db.String(200), nullable= False)
    nome_completo = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
    observacao = db.Column(db.String(500))

    # Relacionamento correto com Activity
    activities = db.relationship('Activity', backref='prospect')

    def __repr__(self):
        return '<name %r' % self.__name__


class CategoryPlan(db.Model):
    __tablename__ = 'category_plan'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(300), nullable=False)
    id_user = db.Column(Integer, ForeignKey('user.id'), nullable=False)
    ativo = db.Column(db.Boolean)

    # Relacionamento com o plano
    plans = db.relationship('Plan', backref='category', lazy=True)

class Plan(db.Model):
    __tablename__ = 'plan'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(300), nullable=False)
    descricao = db.Column(db.Text)
    periodicidade = db.Column(db.String(300))
    preco = db.Column(DECIMAL(10, 2), nullable=False, )
    status = db.Column(db.String(30), nullable=False)
    tipo = db.Column(db.String(100))
    id_category = db.Column(Integer, db.ForeignKey('category_plan.id'), nullable=False)


    def __repr__(self):
        return '<name %r' % self.__name__

