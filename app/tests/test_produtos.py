from app.models import Categoria
from app.extensions import db

def test_criar_produto_sucesso(client, auth_headers):
    categoria = Categoria(nome="Ferramentas")
    db.session.add(categoria)
    db.session.commit()

    resposta = client.post('/produtos', json={
        'nome': 'Parafuso',
        'preco': 1.5,
        'quantidade_estoque': 10,
        'quantidade_minima_estoque': 2,
        'categoria_id': categoria.id
    }, headers=auth_headers)

    assert resposta.status_code == 201
    dados = resposta.get_json()
    assert dados['nome'] ==  'Parafuso'

def test_criar_produto_erro(client, auth_headers):
    categoria = Categoria(nome="Ferramentas")
    db.session.add(categoria)
    db.session.commit()

    resposta = client.post('/produtos', json={
        'nome': 'Parafuso',
        'preco': -1.5,
        'quantidade_estoque': 10,
        'quantidade_minima_estoque': 2,
        'categoria_id': categoria.id
    }, headers=auth_headers)

    assert resposta.status_code == 400
    dados = resposta.get_json()
    assert 'erro' in dados
def test_criar_produto_categoria_inexistente(client, auth_headers):

    resposta = client.post('/produtos', json={
        'nome': 'Parafuso',
        'preco': 1.5,
        'quantidade_estoque': 10,
        'quantidade_minima_estoque': 2,
        'categoria_id': 9999
    }, headers=auth_headers)

    assert resposta.status_code == 400
    dados = resposta.get_json()
    assert 'erro' in dados

def test_listar_produtos_vazio(client, auth_headers):
    resposta = client.get('/produtos')
    assert resposta.status_code == 200
    assert resposta.get_json() == []


def test_listar_produtos_com_itens(client, auth_headers):
    categoria = Categoria(nome="Ferramentas")
    db.session.add(categoria)
    db.session.commit()

    client.post('/produtos', json={
        'nome': 'Parafuso', 'preco': 1.5, 'quantidade_estoque': 10,
        'quantidade_minima_estoque': 2, 'categoria_id': categoria.id
    }, headers=auth_headers)

    resposta = client.get('/produtos')
    dados = resposta.get_json()
    assert resposta.status_code == 200
    assert len(dados) == 1


def test_buscar_produto_nao_encontrado(client, auth_headers):
    resposta = client.get('/produtos/buscar?nome=NaoExiste')
    assert resposta.status_code == 404


def test_atualizar_produto_sucesso(client, auth_headers):
    categoria = Categoria(nome="Ferramentas")
    db.session.add(categoria)
    db.session.commit()

    resposta_criar = client.post('/produtos', json={
        'nome': 'Parafuso', 'preco': 1.5, 'quantidade_estoque':10,
        'quantidade_minima_estoque': 2, 'categoria_id': categoria.id
    }, headers=auth_headers)
    produto_id = resposta_criar.get_json()['id']

    resposta = client.patch(f'/produtos/{produto_id}', json={'preco': 20.0}, headers=auth_headers)
    assert resposta.status_code == 200
    assert resposta.get_json()['produto']['preco'] == '20.00'


def test_atualizar_produto_inexistente(client, auth_headers):
    resposta = client.patch('/produtos/9999', json={'preco': 20.0}, headers=auth_headers)
    assert resposta.status_code == 404


def test_atualizar_produto_sem_campos(client, auth_headers):
    categoria = Categoria(nome="Ferramenta")
    db.session.add(categoria)
    db.session.commit()
    resposta_criar = client.post('/produtos', json={
        'nome': 'Parafuso', 'preco': 1.5,'quantidade_estoque':10,
        'quantidade_minima_estoque': 2, 'categoria_id': categoria.id
    }, headers=auth_headers)
    produto_id = resposta_criar.get_json()['id']

    resposta = client.patch(f'/produtos/{produto_id}', json={}, headers=auth_headers)
    assert resposta.status_code == 400