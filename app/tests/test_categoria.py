
def test_criar_categoria_sucesso(client, auth_headers):
    resposta = client.post('/categorias', json={'nome': 'Ferramentas'}, headers=auth_headers)
    assert resposta.status_code == 201
    dados = resposta.get_json()
    assert dados['nome'] == 'Ferramentas'


def test_criar_categoria_nome_duplicado(client, auth_headers):
    client.post('/categorias', json={'nome': 'Ferramentas'}, headers=auth_headers)
    resposta = client.post('/categorias', json={'nome': 'Ferramentas'}, headers=auth_headers)
    assert resposta.status_code == 400
    assert 'erro' in resposta.get_json()


def test_buscar_categoria_sucesso(client, auth_headers):
    client.post('/categorias', json={'nome': 'Ferramentas'}, headers=auth_headers)
    resposta = client.get('/categorias/buscar?nome=Ferramentas', headers=auth_headers)
    assert resposta.status_code == 200
    assert resposta.get_json()['nome'] == 'Ferramentas'


def test_buscar_categoria_nao_encontrada(client, auth_headers):
    resposta = client.get('/categorias/buscar?nome=NaoExiste', headers=auth_headers)
    assert resposta.status_code == 404


def test_listar_categorias_vazio(client, auth_headers):
    resposta = client.get('/categorias', headers=auth_headers)
    assert resposta.status_code == 200
    assert resposta.get_json() == []


def test_listar_categorias_com_itens(client, auth_headers):
    client.post('/categorias', json={'nome': 'Ferramentas'}, headers=auth_headers)
    resposta = client.get('/categorias', headers=auth_headers)
    dados = resposta.get_json()
    assert resposta.status_code == 200
    assert len(dados) == 1


def test_atualizar_categoria_sucesso(client, auth_headers):
    criada = client.post('/categorias', json={'nome': 'Ferramentas'}, headers=auth_headers)
    categoria_id = criada.get_json()['id']

    resposta = client.patch(f'/categorias/{categoria_id}', json={'nome': 'Ferramentas Grandes'}, headers=auth_headers)
    assert resposta.status_code == 200
    assert resposta.get_json()['categoria']['nome'] == 'Ferramentas Grandes'


def test_atualizar_categoria_inexistente(client, auth_headers):
    resposta = client.patch('/categorias/9999', json={'nome': 'X'}, headers=auth_headers)
    assert resposta.status_code == 404


def test_deletar_categoria_sucesso(client, auth_headers):
    criada = client.post('/categorias', json={'nome': 'Ferramentas'}, headers=auth_headers)
    categoria_id = criada.get_json()['id']

    resposta = client.delete(f'/categorias/{categoria_id}', headers=auth_headers)
    assert resposta.status_code == 200


def test_deletar_categoria_inexistente(client, auth_headers):
    resposta = client.delete('/categorias/9999', headers=auth_headers)
    assert resposta.status_code == 404


def test_deletar_categoria_com_produto_vinculado(client, auth_headers):
    criada = client.post('/categorias', json={'nome': 'Ferramentas'}, headers=auth_headers)
    categoria_id = criada.get_json()['id']

    client.post('/produtos', json={
        'nome': 'Parafuso', 'preco': 1.5, 'quantidade_estoque': 10,
        'quantidade_minima_estoque': 2, 'categoria_id': categoria_id
    }, headers=auth_headers)

    resposta = client.delete(f'/categorias/{categoria_id}', headers=auth_headers)
    assert resposta.status_code == 409
