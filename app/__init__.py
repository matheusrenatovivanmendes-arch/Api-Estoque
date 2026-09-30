import os
from flask import Flask
from dotenv import load_dotenv

from .extensions import db, migrate,limiter,jwt

load_dotenv()


def create_app(config_teste=None):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False  
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    if config_teste:
        app.config.update(config_teste)

    limiter.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from . import models  
    from .routes.produtos_rota import produtos_bp
    app.register_blueprint(produtos_bp)
    from .routes.categoria_rota import categoria_bp
    app.register_blueprint(categoria_bp)
    from .routes.usuario_rota import usuario_bp
    app.register_blueprint(usuario_bp)
    from .routes.login import login_bp
    app.register_blueprint(login_bp)
    from .routes.movimentacao_rota import movimentacao_bp
    app.register_blueprint(movimentacao_bp)
    from .routes.relatorio_rota import relatorio_bp  
    app.register_blueprint(relatorio_bp)
    return app
