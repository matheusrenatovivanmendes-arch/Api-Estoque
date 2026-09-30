from datetime import datetime
from enum import Enum as PyEnum
from passlib.hash import bcrypt
from .extensions import db

class CargoEnum(str, PyEnum):
    ADMIN = "admin"
    OPERADOR = "operador"

class TipoMovimentacaoEnum(str, PyEnum):
    ENTRADA = "entrada"
    SAIDA = "saida"
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False,unique=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.Enum(CargoEnum), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    def set_senha(self, senha_plana: str):
        self.senha_hash = bcrypt.hash(senha_plana)

    def verificar_senha(self, senha_plana: str) -> bool:
        return bcrypt.verify(senha_plana, self.senha_hash)

    def __init__(self, nome: str, username: str, senha: str, cargo: CargoEnum, ativo: bool = True):
        self.nome = nome
        self.username = username
        self.set_senha(senha)
        self.cargo = cargo
        self.ativo = ativo

    def __repr__(self):
        return f'<Usuario {self.id} - {self.username} ({self.cargo}) - ativo={self.ativo}>'
    def to_dict(self):
            return {
                'id': self.id,
                'nome': self.nome,
                'username': self.username,
                'cargo': self.cargo
            }

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(255), nullable=True)

    def __init__(self, nome: str, descricao: str = None):
        self.nome = nome
        self.descricao = descricao

    def __repr__(self):
        return f'<Categoria {self.id} - {self.nome}>'
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao
            }

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False)
    quantidade_minima_estoque = db.Column(db.Integer, nullable=False, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    categoria = db.relationship('Categoria', backref=db.backref('produtos', lazy=True))


    def __init__(self, nome: str, descricao: str, preco: float, quantidade_estoque: int, quantidade_minima_estoque: int, categoria_id: int):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.quantidade_minima_estoque = quantidade_minima_estoque
        self.categoria_id = categoria_id

    def __repr__(self):
        return f'<Produto {self.id} - {self.nome} - Preço: {self.preco} - Estoque: {self.quantidade_estoque}>'
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'quantidade_estoque': self.quantidade_estoque,
            'quantidade_minima_estoque': self.quantidade_minima_estoque,
            'estoque_baixo': self.quantidade_estoque <= self.quantidade_minima_estoque
        }
class Historico(db.Model):
    __tablename__ = 'historico'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    produto = db.relationship('Produto', backref=db.backref('historico', lazy=True))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    quantidade_alterada = db.Column(db.Integer, nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    tipo_movimentacao = db.Column(db.Enum(TipoMovimentacaoEnum), nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2),nullable=True) 
                               
    usuario = db.relationship('Usuario', backref=db.backref('historico', lazy=True))

    def __init__(self,produto_id: int,usuario_id: int, quantidade_alterada: int, tipo_movimentacao: TipoMovimentacaoEnum,preco_unitario: float | None  = None):
        self.produto_id = produto_id
        self.preco_unitario=preco_unitario
        self.usuario_id = usuario_id
        self.quantidade_alterada = quantidade_alterada
        self.tipo_movimentacao = tipo_movimentacao

    def __repr__(self):
        return f'<Historico {self.id} - Produto ID: {self.produto_id} - Quantidade Alterada: {self.quantidade_alterada} - Data/Hora: {self.data_hora} - Tipo: {self.tipo_movimentacao}>'

