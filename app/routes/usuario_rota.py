from flask import Blueprint, jsonify, request
from app.models import CargoEnum
from app.auth import requer_cargo
from pydantic import ValidationError
from app.shemas.schemas import UsuarioSchema,AtualizarUsuarioSchema,ProcurarUsuarioSchema
from app.services.usuario import criar_usuario,todos_usuarios,atualizar_usuario,deletar_usuario,buscar_usuario

usuario_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuario_bp.route('', methods=['POST'])
@requer_cargo(CargoEnum.ADMIN)
def criar_usuario_rota():
    dados = request.get_json() 
    if not dados:
        return jsonify({"erro": "Dados inválidos."}), 400
    try:
        usuario_shema = UsuarioSchema(**dados)
        usuario = criar_usuario(usuario_shema)
        resposta = {
                'id': usuario.id,
                'nome': usuario.nome,
                'username': usuario.username,
                'cargo': usuario.cargo
                }
        return jsonify(resposta), 201
    except ValidationError as e:
        return jsonify({"erro": str(e)}), 400
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@usuario_bp.route('/buscar', methods=['GET'])
@requer_cargo(CargoEnum.ADMIN)
def buscar_usuario_rota():
    username = request.args.get('username')
    if not username:
        return jsonify({"erro": "Parâmetro 'nome' é obrigatório."}), 400
    try:
        dados = ProcurarUsuarioSchema(username=username)
        usuario = buscar_usuario(dados)
        resposta = {
            'id': usuario.id,
            'nome': usuario.nome,
            'username': usuario.username,
            'cargo': usuario.cargo,
        } 
        return jsonify(resposta), 200
    except ValidationError as e:
        return jsonify({"erro": str(e)}), 400
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404

    
@usuario_bp.route('', methods=['GET'])
@requer_cargo(CargoEnum.ADMIN)
def usuarios_todos_rotas():
    usuarios = todos_usuarios()
    resultados = []
    for p in usuarios:
        resultados.append({
            'id': p.id,
            'nome': p.nome,
            'username': p.username,
            'cargo': p.cargo,
            })
    return jsonify(resultados), 200

@usuario_bp.route('/<int:id>', methods=['PATCH'])
@requer_cargo(CargoEnum.ADMIN)
def atualizar_usuario_rota(id: int):
  try:
    dados_json = request.get_json()
    usuario_valido = AtualizarUsuarioSchema(**dados_json)
  except ValidationError as e:
    return (
        jsonify({
            'erro': 'Erro de validação nos campos informados',
            'detalhes': e.errors(),
        }),
        400,
    )

  campos_para_atualizar = usuario_valido.model_dump(exclude_unset=True)

  if not campos_para_atualizar:
    return (
        jsonify({'aviso': 'Nenhum campo válido foi enviado para atualização'}),
        400,
    )

  try:
    usuario_atualizado = atualizar_usuario(id, campos_para_atualizar)
    return jsonify({
        'mensagem': f'Produto {id} atualizado com sucesso!',
        'usuario': usuario_atualizado.to_dict(),  
    })
  except ValueError as e:
    return jsonify({'erro': str(e)}), 404

@usuario_bp.route('/<int:id>', methods=['DELETE'])
@requer_cargo(CargoEnum.ADMIN)
def deletar_usuario_rota(id: int):
  try:
      usuario_deletar = deletar_usuario(id)
      return jsonify({
          'mensagem': f'Usuario {id} deletado com sucesso!'
      })
  except ValueError as e:
      return jsonify({'erro': str(e)}), 404

    