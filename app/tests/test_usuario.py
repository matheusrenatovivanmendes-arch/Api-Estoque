from app.models import Usuario
from app.extensions import db


def test_criar_usuario_sucesso(client, auth_headers):
    resposta = client.post('/usuarios', json={
        'nome': 'Joao', 'username': 'joao', 'senha': '12345678', 'cargo': 'operador'
    }, headers=auth_headers)
    assert resposta.status_code == 201
    dados = resposta.get_json()
    assert dados['username'] == 'joao'
    assert 'senha' not in dados


def test_criar_usuario_username_duplicado(client, auth_headers):
    client.post('/usuarios', json={
        'nome': 'Joao', 'username': 'joao', 'senha': '12345678', 'cargo': 'operador'
    }, headers=auth_headers)
    resposta = client.post('/usuarios', json={
        'nome': 'Outro', 'username': 'joao', 'senha': '87654321', 'cargo': 'operador'
    }, headers=auth_headers)
    assert resposta.status_code == 400
    assert 'erro' in resposta.get_json()


def test_buscar_usuario_sucesso(client, auth_headers):
    client.post('/usuarios', json={
        'nome': 'Joao', 'username': 'joao', 'senha': '12345678', 'cargo': 'operador'
    }, headers=auth_headers)
    resposta = client.get('/usuarios/buscar?username=joao', headers=auth_headers)
    assert resposta.status_code == 200
    assert resposta.get_json()['username'] == 'joao'


def test_buscar_usuario_nao_encontrado(client, auth_headers):
    resposta = client.get('/usuarios/buscar?username=naoexiste', headers=auth_headers)
    assert resposta.status_code == 404


def test_listar_usuarios(client, auth_headers):
    # auth_headers ja cria 1 usuario admin pra logar
    resposta = client.get('/usuarios', headers=auth_headers)
    assert resposta.status_code == 200
    assert len(resposta.get_json()) == 1


def test_atualizar_usuario_sucesso(client, auth_headers):
    criado = client.post('/usuarios', json={
        'nome': 'Joao', 'username': 'joao', 'senha': '12345678', 'cargo': 'operador'
    }, headers=auth_headers)
    usuario_id = criado.get_json()['id']

    resposta = client.patch(f'/usuarios/{usuario_id}', json={'nome': 'Joao Silva'}, headers=auth_headers)
    assert resposta.status_code == 200
    assert resposta.get_json()['usuario']['nome'] == 'Joao Silva'


def test_atualizar_usuario_senha(client, auth_headers):
    criado = client.post('/usuarios', json={
        'nome': 'Joao', 'username': 'joao', 'senha': '12345678', 'cargo': 'operador'
    }, headers=auth_headers)
    usuario_id = criado.get_json()['id']

    client.patch(f'/usuarios/{usuario_id}', json={'senha': 'novaSenha1'}, headers=auth_headers)

    usuario = db.session.query(Usuario).filter_by(id=usuario_id).first()
    assert usuario.verificar_senha('novaSenha1') is True
    assert usuario.verificar_senha('12345678') is False


def test_atualizar_usuario_inexistente(client, auth_headers):
    resposta = client.patch('/usuarios/9999', json={'nome': 'X'}, headers=auth_headers)
    assert resposta.status_code == 404


def test_deletar_usuario_sucesso(client, auth_headers):
    criado = client.post('/usuarios', json={
        'nome': 'Joao', 'username': 'joao', 'senha': '12345678', 'cargo': 'operador'
    }, headers=auth_headers)
    usuario_id = criado.get_json()['id']

    resposta = client.delete(f'/usuarios/{usuario_id}', headers=auth_headers)
    assert resposta.status_code == 200


def test_deletar_usuario_inexistente(client, auth_headers):
    resposta = client.delete('/usuarios/9999', headers=auth_headers)
    assert resposta.status_code == 404
