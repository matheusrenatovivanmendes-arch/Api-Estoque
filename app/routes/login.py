from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from pydantic import BaseModel, ValidationError
from app.extensions import limiter
from app.services.autentificar import autenticar

login_bp = Blueprint('usuario', __name__, url_prefix='/usuario')


class LoginInput(BaseModel):
    username: str
    senha: str


@login_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login_route():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'envie os dados em JSON'}), 400

    try:
        dados_validados = LoginInput(**dados)
    except ValidationError as e:
        return jsonify({'erro': e.errors()}), 400
    try:
        usuario = autenticar(
            username=dados_validados.username,
            senha=dados_validados.senha
        )
    except ValueError as e:
        return jsonify({'erro': str(e)}), 401

    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={'cargo': usuario.cargo.value}
    )

    resposta = jsonify({
        'nome': usuario.nome,
        'username': usuario.username,
        'cargo': usuario.cargo.value
    })
    set_access_cookies(resposta, token)
    return resposta, 200


@login_bp.route('/logout', methods=['POST'])
def logout_route():
    resposta = jsonify({'mensagem': 'Sessão encerrada.'})
    unset_jwt_cookies(resposta)
    return resposta, 200