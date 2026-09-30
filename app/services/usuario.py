from app.extensions import db
from app.models import Usuario
from app.shemas.schemas import UsuarioSchema,AtualizarUsuarioSchema,ProcurarUsuarioSchema
from sqlalchemy import func

def criar_usuario(dados: UsuarioSchema):
    username = db.session.query(Usuario).filter(func.lower(Usuario.username) == dados.username.strip().lower()).first()
    if username:
        raise ValueError('nome de usuario ja existe')
    usuario = Usuario(nome=dados.nome,username=dados.username,senha=dados.senha,cargo=dados.cargo)
    db.session.add(usuario)
    db.session.commit()
    return usuario
def todos_usuarios():
    usuarios = db.session.query(Usuario).all()
    return usuarios

def buscar_usuario(dados: ProcurarUsuarioSchema):
    usuario_existe = db.session.query(Usuario).filter(func.lower(Usuario.username) == dados.username.strip().lower()).first()
    if not usuario_existe:
        raise ValueError('username nao existe')
    return usuario_existe
def atualizar_usuario(usuario_id: int, campos_para_atualizar: dict):
    usuario_existe = db.session.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario_existe:
       raise ValueError('usuario nao existe')
    for campo, valor in campos_para_atualizar.items():
        if campo == 'senha':
            usuario_existe.set_senha(valor)
        else:
            setattr(usuario_existe, campo, valor)
    db.session.commit()
    return usuario_existe

def deletar_usuario(usuario_id: int):
    usuario = db.session.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        raise ValueError('usuario nao existe')
    db.session.delete(usuario)
    db.session.commit()