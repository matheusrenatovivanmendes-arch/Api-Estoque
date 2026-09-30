from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import CSRFError
import os

def requer_cargo(*cargos_permitidos):
    def decorator(funcao):
        @wraps(funcao)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            cargo_usuario = claims.get('cargo')

            if cargo_usuario not in [c.value for c in cargos_permitidos]:
                return jsonify({'erro': 'sem permissao para essa acao'}), 403

            return funcao(*args, **kwargs)
        return wrapper
    return decorator
