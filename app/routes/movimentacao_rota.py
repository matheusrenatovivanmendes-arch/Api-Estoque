from pydantic import ValidationError
from flask import Blueprint, jsonify, request
from app.models import CargoEnum,TipoMovimentacaoEnum
from app.auth import requer_cargo
from app.shemas.schemas import MovimentacaoSchema
from app.services.movimentacao import registrar_movimentacao
from flask_jwt_extended import get_jwt_identity


movimentacao_bp = Blueprint('movimentacao', __name__, url_prefix='/movimentacao')

@movimentacao_bp.route('', methods=['POST'])
@requer_cargo(CargoEnum.ADMIN, CargoEnum.OPERADOR)
def registrar_movimentacao_rota():
    dados = request.get_json() 
    usuario_id = int(get_jwt_identity())
    if not dados:
        return jsonify({"erro": "Dados inválidos."}), 400
    try:
        movimentacao_shema = MovimentacaoSchema(**dados)
        movimentacao = registrar_movimentacao(movimentacao_shema,usuario_id)
        resposta = {
                'id': movimentacao.id,
                }
        return jsonify(resposta), 201
    except ValidationError as e:
        return jsonify({"erro": str(e)}), 400
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400