from app.extensions import db
from app.models import Usuario


def autenticar(username: str, senha: str):
    if username is None or senha is None:
        raise ValueError("Todos os campos são obrigatórios.")

    usuario = db.session.query(Usuario).filter_by(username=username).first()
    if not usuario or not usuario.verificar_senha(senha):
        raise ValueError("Credenciais inválidas.")

    return usuario
