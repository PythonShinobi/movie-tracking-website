"""Initialize Flask extensions used throughout the application.

This module creates extension instances independently of the Flask
application so they can be initialized later by the application factory.
This avoids coupling the extensions to a specific application instance.

Examples:
    - SQLAlchemy: Provides database access and ORM functionality.
    - CSRFProtect: Provides protection against cross-site request forgery.
    - Migrate: Provides database migration support.
    - Bootstrap: Provides Bootstrap integration for Flask templates.
    - LoginManager: Manages user authentication and login sessions.
"""

from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

csrf = CSRFProtect()

bootstrap = Bootstrap()

migrate = Migrate()

login_manager = LoginManager()
# Flask-Login will know where to send an unauthenticated user 
# if they try to access a protected page.
login_manager.login_view = "auth.login"