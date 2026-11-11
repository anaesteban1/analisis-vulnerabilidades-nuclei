"""Aplicación EstadoSeguro."""

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev-only-change-me",
        DEBUG=False,
    )
    if test_config:
        app.config.update(test_config)

    from .routes import bp

    app.register_blueprint(bp)
    return app
