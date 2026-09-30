from app.extensions import db
from app.models import Produto, Categoria, Historico
from app.exceptions import ConflitoDeRecurso
from app.shemas.schemas import ProdutoSchema,ProcurarProdutoSchema,AtualizarProdutoSchema
from sqlalchemy import func

def criar_produto(dados: ProdutoSchema):
    categoria_existe = db.session.query(Categoria).filter_by(id=dados.categoria_id).first()
    if not categoria_existe:
        raise ValueError('categoria_id nao existe')
    nome_existe = db.session.query(Produto).filter(func.lower(Produto.nome) == dados.nome.strip().lower()).first()
    if nome_existe:
        raise ValueError('nome ja existe')
    produto = Produto(nome=dados.nome, descricao=dados.descricao, preco=dados.preco, quantidade_estoque = dados.quantidade_estoque, quantidade_minima_estoque = dados.quantidade_minima_estoque, categoria_id= dados.categoria_id)
    db.session.add(produto)
    db.session.commit()
    return produto
def buscar_produto(dados: ProcurarProdutoSchema):
    produto_existe = db.session.query(Produto).filter(func.lower(Produto.nome) == dados.nome.strip().lower()).first()
    if not produto_existe:
        raise ValueError('produto nao existe')
    return produto_existe
def produtos_todos():
    produtos = db.session.query(Produto).all()
    return produtos

def atualizar_produto(produto_id: int, campos_para_atualizar: dict):
    if campos_para_atualizar.get('categoria_id'):
        categoria_existe = db.session.query(Categoria).filter_by(id=campos_para_atualizar.get('categoria_id')).first()
        if not categoria_existe:
            raise ValueError('categoria_id nao existe')
    produto = db.session.query(Produto).filter_by(id=produto_id).first()
    if not produto:
        raise ValueError('produto nao existe')

    for campo, valor in campos_para_atualizar.items():
        setattr(produto, campo, valor)

    db.session.commit()
    return produto

def deletar_produto(produto_id: int):
    produto = db.session.query(Produto).filter_by(id=produto_id).first()
    historico = db.session.query(Historico).filter_by(produto_id=produto_id).first()
    if not produto:
        raise ValueError('produto nao existe')
    if historico:
        raise ConflitoDeRecurso('produto ja vinculado')
    db.session.delete(produto)
    db.session.commit()