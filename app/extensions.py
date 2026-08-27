"""Initialize Flask extensions used throughout the application."""

from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

csrf = CSRFProtect()