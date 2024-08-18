from application import db
from datetime import datetime


class Prospect(db.Model):
    __tablename__ = 'prospect'
    id = db.Column(db.Integer, primary_key=True)
    data_hora_cadastro = db.Column(db.DateTime, default=datetime.now)
    email = db.Column(db.String(200), nullable= False)
    nome_completo = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
    observacao = db.Column(db.String(500))

    def __repr__(self):
        return '<name %r' % self.__name__
