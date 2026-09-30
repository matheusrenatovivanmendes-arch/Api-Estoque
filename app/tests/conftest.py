import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    app = create_app(config_teste={
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",   # <- qual URI de banco você quer usar só pro teste?
        "TESTING": True,
    })

    with app.app_context():
        db.create_all()   # cria as tabelas nesse banco de teste
        yield app          # "pausa" aqui, entrega o app pronto pro teste rodar
        db.drop_all()
@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    from app.services.usuario import criar_usuario
    from app.shemas.schemas import UsuarioSchema

    criar_usuario(UsuarioSchema(nome='Admin Teste', username='admin_teste', senha='12345678', cargo='admin'))
    client.post('/usuario/login', json={'username': 'admin_teste', 'senha': '12345678'})
    csrf = client.get_cookie('csrf_access_token').value
    return {'X-CSRF-TOKEN': csrf}