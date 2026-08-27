"""Initialize Flask extensions used throughout the application."""

from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

csrf = CSRFProtect()

bootstrap = Bootstrap()

login_manager = LoginManager()

migrate = Migrate()