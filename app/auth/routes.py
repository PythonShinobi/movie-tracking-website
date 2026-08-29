"""HTTP routes for authentication."""

from flask import jsonify, request

from app.extensions import db
from app.auth import auth as auth_blueprint
from app.adapters.repository import UserRepository
from app.adapters.password_hasher import PasswordHasher
from app.services.authentication import AuthenticationService


@auth_blueprint.route("/register", methods=["POST"])
def register():
    """Register a new user."""

    data = request.get_json()

    service = AuthenticationService(
        repository=UserRepository(),
        password_hasher=PasswordHasher()
    )

    user = service.register(
        email=data["email"],
        username=data["username"],
        password=data["password"]
    )

    db.session.commit()

    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username,
    }), 201