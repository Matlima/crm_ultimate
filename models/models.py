from application import db
from datetime import datetime



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
    id = db.Column(db.Integer, primary_key=True, unique=True)
    razao_social = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(200), nullable=False)
    cpfecnpj = db.Column(db.String(30))
    inscricao_estadual = db.Column(db.String(50))
    inscricao_municipal = db.Column(db.String(50))
    telefone = db.Column(db.String(50))
    celular = db.Column(db.String(50))
    email = db.Column(db.String(100))
    tipo_conta = db.Column(db.String(20))
    endereco = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(5))
    numero = db.Column(db.String(10))
    cep = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    activities = db.relationship('Activity', backref='cliente', lazy=True)

    def __repr__(self):
        return '<name %r' % self.__name__

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_inicio = db.Column(db.DateTime, default=datetime.now)
    data_fim = db.Column(db.DateTime)
    tipo = db.Column(db.String(100))
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    status = db.Column(db.String(20))

    def __repr__(self):
        return '<name %r' % self.__name__





