"""HTTP routes for authentication."""

from flask import jsonify

from app.auth import auth as auth_blueprint

@auth_blueprint.route("/register", methods=["POST"])
def register():
    """Handle user registration requests."""

    return jsonify({"message": "Registration endpoint"})