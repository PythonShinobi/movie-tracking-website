"""Authentication blueprint for user registration and authentication."""

from flask import Blueprint

from app.extensions import login_manager
from app.adapters.orm import UserModelRecord
from app.adapters.flask_login_user import FlaskLoginUser
from app.adapters.mappers import user_model_record_to_user_object


auth = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    """Load a Flask-Login user from the database using their ID."""
    record = UserModelRecord.query.get(int(user_id))

    if record is None:
        return None

    user = user_model_record_to_user_object(record)

    return FlaskLoginUser(user)


from app.auth import routes