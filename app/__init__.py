"""Create and configure the Flask application using the application factory pattern."""

from flask import Flask, render_template

from app.config import config
from app.auth import auth as auth_blueprint
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
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register authentication blueprint with application.
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    @app.errorhandler(404)
    def page_not_found(error):
        """Render the custom page shown when a requested page does not exist."""
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Render the custom page shown when an internal server error occurs."""
        db.session.rollback()
        return render_template("errors/500.html"), 500

    return app