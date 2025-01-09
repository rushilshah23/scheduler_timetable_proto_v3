from flask import Flask
from .config import AppConfig
from .init_celery import celery_init_app
from .blueprint import bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    app.config.from_prefixed_env()
    celery_init_app(app)

    app.register_blueprint(bp,url_prefix="/operations")

    return app


