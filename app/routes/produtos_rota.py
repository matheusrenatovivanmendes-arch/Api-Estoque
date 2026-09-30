from pydantic import ValidationError
from flask import Blueprint, jsonify, request
from app.models import CargoEnum
from app.exceptions import ConflitoDeRecurso
from app.auth import requer_cargo
from app.shemas.schemas import ProdutoSchema, ProcurarProdutoSchema,AtualizarProdutoSchema
from app.services.produtos import criar_produto, buscar_produto,produtos_todos,atualizar_produto,deletar_produto

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@produtos_bp.route('', methods=['POST'])
@requer_cargo(CargoEnum.ADMIN)
def criar_produto_rota():
    dados = request.get_json() #Obtém os dados da requisição
    #Valida os dados recebidos
    if not dados:
        return jsonify({"erro": "Dados inválidos."}), 400
    try:
        produto_schema = ProdutoSchema(**dados)
        produto = criar_produto(produto_schema)
        estoque_baixo = produto.quantidade_estoque <= produto.quantidade_minima_estoque
        resposta = {
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'preco': produto.preco,
            'quantidade_estoque': produto.quantidade_estoque,
            'quantidade_minima_estoque': produto.quantidade_minima_estoque,
            'estoque_baixo': estoque_baixo
        }
        return jsonify(resposta), 201
    except ValidationError as e:
        return jsonify({"erro": str(e)}), 400
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    
@produtos_bp.route('/buscar', methods=['GET'])
@requer_cargo(CargoEnum.ADMIN)
def buscar_produto_rota():
    nome = request.args.get('nome')
    if not nome:
        return jsonify({"erro": "Parâmetro 'nome' é obrigatório."}), 400
    try:
        dados = ProcurarProdutoSchema(nome=nome)
        produto = buscar_produto(dados)
        estoque_baixo = produto.quantidade_estoque <= produto.quantidade_minima_estoque
        resposta = {
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'preco': produto.preco,
            'quantidade_estoque': produto.quantidade_estoque,
            'quantidade_minima_estoque': produto.quantidade_minima_estoque,
            'estoque_baixo': estoque_baixo
        } 
        return jsonify(resposta), 200
    except ValidationError as e:
        return jsonify({"erro": str(e)}), 400
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    
@produtos_bp.route('', methods=['GET'])
@requer_cargo(CargoEnum.ADMIN)
def produtos_todos_rotas():
    produtos = produtos_todos()
    resultados = []
    for p in produtos:
        resultados.append({
            'id': p.id,
            'nome': p.nome,
            'descricao': p.descricao,
            'preco': p.preco,
            'quantidade_estoque': p.quantidade_estoque,
            'quantidade_minima_estoque': p.quantidade_minima_estoque,
            'estoque_baixo':  p.quantidade_estoque <= p.quantidade_minima_estoque
            })
    return jsonify(resultados), 200
@produtos_bp.route('/<int:id>', methods=['PATCH'])
@requer_cargo(CargoEnum.ADMIN)
def atualizar_produto_rota(id: int):
  try:
    dados_json = request.get_json()
    produto_valido = AtualizarProdutoSchema(**dados_json)
  except ValidationError as e:
    return (
        jsonify({
            'erro': 'Erro de validação nos campos informados',
            'detalhes': e.errors(),
        }),
        400,
    )

  campos_para_atualizar = produto_valido.model_dump(exclude_unset=True)

  if not campos_para_atualizar:
    return (
        jsonify({'aviso': 'Nenhum campo válido foi enviado para atualização'}),
        400,
    )

  try:
    produto_atualizado = atualizar_produto(id, campos_para_atualizar)
    return jsonify({
        'mensagem': f'Produto {id} atualizado com sucesso!',
        'produto': produto_atualizado.to_dict(),  
    })
  except ValueError as e:
    return jsonify({'erro': str(e)}), 404

@produtos_bp.route('/<int:id>', methods=['DELETE'])
@requer_cargo(CargoEnum.ADMIN)
def deletar_produto_rota(id: int):
  try:
      produto_deletar = deletar_produto(id)
      return jsonify({
          'mensagem': f'Produto {id} deletado com sucesso!'
      })
  except ValueError as e:
      return jsonify({'erro': str(e)}), 404
  except ConflitoDeRecurso as e:
      return jsonify({'erro': str(e)}), 409