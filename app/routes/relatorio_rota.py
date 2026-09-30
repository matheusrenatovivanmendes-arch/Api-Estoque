from pydantic import ValidationError
from flask import Blueprint, jsonify,request,send_file
from app.models import CargoEnum
from app.auth import requer_cargo
from app.shemas.schemas import RelatorioFaturamentoSchema
from app.services.relatorio import relatorio


relatorio_bp = Blueprint('relatorio', __name__, url_prefix='/relatorio')

@relatorio_bp.route('', methods=['GET'])
@requer_cargo(CargoEnum.ADMIN)
def relatorio_rota():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    dados = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    if not dados:
        return jsonify({"erro": "Dados inválidos."}), 400
    try:
        relatorio_shema = RelatorioFaturamentoSchema(**dados)
        relatorio_ = relatorio(relatorio_shema)
        resposta = send_file(
            relatorio_,
            as_attachment=True,
            download_name='relatorio_faturamento.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        return resposta
    except ValidationError as e:
        return jsonify({"erro": str(e)}), 400
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
