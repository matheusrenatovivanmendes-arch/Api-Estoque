from app import create_app
from app.extensions import db
from app.services.usuario import criar_usuario
from app.shemas.schemas import UsuarioSchema
from app.models import Usuario

app = create_app()

with app.app_context():
    existe = db.session.query(Usuario).filter_by(username='admin').first()
    if existe:
        print('Usuario admin ja existe, nada foi feito.')
    else:
        usuario = criar_usuario(UsuarioSchema(
            nome='Administrador',
            username='admin',
            senha='admin12345',
            cargo='admin'
        ))
        print(f'Usuario admin criado com sucesso! id={usuario.id}, username={usuario.username}')
        print('Senha: admin12345 -- troque isso depois do primeiro login.')
