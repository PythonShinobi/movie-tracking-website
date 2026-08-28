"""Initialize Flask extensions used throughout the application."""

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