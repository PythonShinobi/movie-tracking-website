"""Create and configure the Flask application using the application factory pattern."""

from flask import Flask

from app.config import config
from app.extensions import (
    db, 
    csrf,
    migrate,
    bootstrap,
    login_manager,
)


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)

    # Load configuration settings into Flask application configuration.
    app.config.from_object(config[config_name])

    # Perform application-specific initialization.
    config[config_name].init_app(app)

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    return app