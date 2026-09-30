from pydantic import ValidationError
from flask import Blueprint, jsonify, request
from app.models import CargoEnum
from app.auth import requer_cargo
from app.shemas.schemas import CategoriaSchema, AtualizarCategoriaSchema,ProcurarCategoriaSchema
from app.exceptions import RecursoNaoEncontrado, ConflitoDeRecurso 
from app.services.categoria import criar_categoria, categorias_todos, buscar_categoria,atualizar_categoria,deletar_categoria

categoria_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@categoria_bp.route('', methods=['POST'])
@requer_cargo(CargoEnum.ADMIN)
def criar_categoria_rota():
    dados = request.get_json() 
    if not dados:
        return jsonify({"erro": "Dados inválidos."}), 400
    try:
        categoria_schema = CategoriaSchema(**dados)
        categoria = criar_categoria(categoria_schema)
        resposta = {
            'id': categoria.id,
            'nome': categoria.nome,
            'descricao': categoria.descricao
        }
        return jsonify(resposta), 201
    except ValidationError as e:
        return jsonify({"erro": str(e)}), 400
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@categoria_bp.route('/buscar', methods=['GET'])
@requer_cargo(CargoEnum.ADMIN)
def buscar_categoria_rota():
    nome = request.args.get('nome')
    if not nome:
        return jsonify({"erro": "Parâmetro 'nome' é obrigatório."}), 400
    try:
        dados = ProcurarCategoriaSchema(nome=nome)
        categoria = buscar_categoria(dados)
        resposta = {
            'id': categoria.id,
            'nome': categoria.nome,
            'descricao': categoria.descricao,
        } 
        return jsonify(resposta), 200
    except ValidationError as e:
        return jsonify({"erro": str(e)}), 400
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    
@categoria_bp.route('', methods=['GET'])
@requer_cargo(CargoEnum.ADMIN)
def categorias_todos_rotas():
    categorias = categorias_todos()
    resultados = []
    for p in categorias:
        resultados.append({
            'id': p.id,
            'nome': p.nome,
            'descricao': p.descricao,
            })
    return jsonify(resultados), 200

@categoria_bp.route('/<int:id>', methods=['PATCH'])
@requer_cargo(CargoEnum.ADMIN)
def atualizar_categoria_rota(id: int):
  try:
    dados_json = request.get_json()
    categoria_valido = AtualizarCategoriaSchema(**dados_json)
  except ValidationError as e:
    return (
        jsonify({
            'erro': 'Erro de validação nos campos informados',
            'detalhes': e.errors(),
        }),
        400,
    )

  campos_para_atualizar = categoria_valido.model_dump(exclude_unset=True)

  if not campos_para_atualizar:
    return (
        jsonify({'aviso': 'Nenhum campo válido foi enviado para atualização'}),
        400,
    )

  try:
    categoria_atualizado = atualizar_categoria(id, campos_para_atualizar)
    return jsonify({
        'mensagem': f'Categoria {id} atualizado com sucesso!',
        'categoria': categoria_atualizado.to_dict(),  
    })
  except ValueError as e:
    return jsonify({'erro': str(e)}), 404
@categoria_bp.route('/<int:id>', methods=['DELETE'])
@requer_cargo(CargoEnum.ADMIN)
def deletar_produto_rota(id: int):
  try:
      categoria_deletar = deletar_categoria(id)
      return jsonify({
          'mensagem': f'Categoria {id} deletada com sucesso!'
      })
  except RecursoNaoEncontrado as e:
    return jsonify({'erro': str(e)}), 404
  except ConflitoDeRecurso as e:
    return jsonify({'erro': str(e)}), 409