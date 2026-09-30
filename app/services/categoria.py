from app.extensions import db
from app.models import Categoria,Produto
from app.shemas.schemas import CategoriaSchema,ProcurarCategoriaSchema
from app.exceptions import RecursoNaoEncontrado, ConflitoDeRecurso
from sqlalchemy import func

def criar_categoria(dados: CategoriaSchema):
    categoria_existe = db.session.query(Categoria).filter(func.lower(Categoria.nome) == dados.nome.strip().lower()).first()
    if categoria_existe:
        raise ValueError('nome ja existe')
    categoria = Categoria(nome=dados.nome, descricao=dados.descricao)
    db.session.add(categoria)
    db.session.commit()
    return categoria

def buscar_categoria(dados: ProcurarCategoriaSchema):
    categoria_existe = db.session.query(Categoria).filter(func.lower(Categoria.nome) == dados.nome.strip().lower()).first()
    if not categoria_existe:
        raise ValueError('categoria nao existe')
    return categoria_existe
def categorias_todos():
    categorias = db.session.query(Categoria).all()
    return categorias

def atualizar_categoria(produto_id: int, campos_para_atualizar: dict):
    categoria = db.session.query(Categoria).filter_by(id=produto_id).first()
    if not categoria:
        raise ValueError('categoria nao existe')

    for campo, valor in campos_para_atualizar.items():
        setattr(categoria, campo, valor)

    db.session.commit()
    return categoria


def deletar_categoria(categoria_id: int):
    categoria = db.session.query(Categoria).filter_by(id=categoria_id).first()
    produtos = db.session.query(Produto).filter_by(categoria_id=categoria_id).first()
    if not categoria:
        raise RecursoNaoEncontrado('categoria nao existe')
    if produtos:
        raise ConflitoDeRecurso('categoria esta vinculado ao um produto')
    db.session.delete(categoria)
    db.session.commit()