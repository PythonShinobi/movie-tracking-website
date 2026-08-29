"""Authentication blueprint for user registration and authentication."""

from flask import Blueprint

from app.extensions import login_manager
from app.adapters.orm import UserModelRecord

auth = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    """Load a user from the database using their ID."""
    return UserModelRecord.query.get(int(user_id))

from app.auth import routes