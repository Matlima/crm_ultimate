from application import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name



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

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(Integer, primary_key=True)
    cliente_id = db.Column(Integer, ForeignKey('customer.id'), nullable=False)
    usuario_id = db.Column(Integer, ForeignKey('user.id'), nullable=False)
    data_inicio = db.Column(DateTime, default=datetime.now)
    data_fim = db.Column(DateTime)
    tipo = db.Column(String(100))
    titulo = db.Column(String(100))
    descricao = db.Column(db.Text)
    status = db.Column(String(20))

    def __repr__(self):
        return '<name %r' % self.__name__





