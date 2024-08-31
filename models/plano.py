from application import db
from datetime import datetime
from sqlalchemy import DECIMAL


class Plano(db.Model):
    __tablename__ = 'planos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(300), nullable=False)
    descricao = db.Column(db.Text)
    periodicidade = db.Column(db.String(300))
    preco = db.Column(DECIMAL(10, 2), nullable=False, )
    status = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<name %r' % self.__name__