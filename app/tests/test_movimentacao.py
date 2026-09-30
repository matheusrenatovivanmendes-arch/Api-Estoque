from app.models import Categoria
from app.extensions import db


def _criar_produto(client, auth_headers, quantidade_estoque=10):
    categoria = Categoria(nome="Ferramentas")
    db.session.add(categoria)
    db.session.commit()

    criado = client.post('/produtos', json={
        'nome': 'Parafuso', 'preco': 1.5, 'quantidade_estoque': quantidade_estoque,
        'quantidade_minima_estoque': 2, 'categoria_id': categoria.id
    }, headers=auth_headers)
    return criado.get_json()['id']


def test_registrar_entrada_sucesso(client, auth_headers):
    produto_id = _criar_produto(client, auth_headers, quantidade_estoque=10)

    resposta = client.post('/movimentacao', json={
        'produto_id': produto_id, 'quantidade': 20, 'tipo_movimentacao': 'entrada'
    }, headers=auth_headers)
    assert resposta.status_code == 201

    produto = client.get('/produtos/buscar?nome=Parafuso', headers=auth_headers).get_json()
    assert produto['quantidade_estoque'] == 30


def test_registrar_saida_sucesso(client, auth_headers):
    produto_id = _criar_produto(client, auth_headers, quantidade_estoque=10)

    resposta = client.post('/movimentacao', json={
        'produto_id': produto_id, 'quantidade': 5, 'tipo_movimentacao': 'saida'
    }, headers=auth_headers)
    assert resposta.status_code == 201

    produto = client.get('/produtos/buscar?nome=Parafuso', headers=auth_headers).get_json()
    assert produto['quantidade_estoque'] == 5


def test_registrar_saida_estoque_insuficiente(client, auth_headers):
    produto_id = _criar_produto(client, auth_headers, quantidade_estoque=10)

    resposta = client.post('/movimentacao', json={
        'produto_id': produto_id, 'quantidade': 999, 'tipo_movimentacao': 'saida'
    }, headers=auth_headers)
    assert resposta.status_code == 400
    assert 'erro' in resposta.get_json()


def test_registrar_movimentacao_produto_inexistente(client, auth_headers):
    resposta = client.post('/movimentacao', json={
        'produto_id': 9999, 'quantidade': 5, 'tipo_movimentacao': 'entrada'
    }, headers=auth_headers)
    assert resposta.status_code == 400
    assert 'erro' in resposta.get_json()


def test_registrar_movimentacao_sem_login(client):
    resposta = client.post('/movimentacao', json={
        'produto_id': 1, 'quantidade': 5, 'tipo_movimentacao': 'entrada'
    })
    assert resposta.status_code == 401
