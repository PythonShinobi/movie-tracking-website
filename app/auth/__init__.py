"""Authentication blueprint for user registration and authentication."""

from flask import Blueprint

auth = Blueprint("auth", __name__)

from app.auth import routes