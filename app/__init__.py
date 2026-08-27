from flask import Flask

from app.config import config

def create_app(config_name: str ="default") -> Flask:
    app = Flask(__name__)

    # Load configuration settings into flask application configuration.
    app.config.from_object(config[config_name])

    # Perform application-specific initialization.
    config[config_name].init_app(app)

    return app