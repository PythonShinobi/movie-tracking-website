from flask import render_template
from flask_login import current_user, login_required

from app.main import main as main_blueprint

@main_blueprint.route("/")
def home():
    return render_template("main/home.html")

@main_blueprint.route("/profile")
@login_required
def profile():
    return {
        "email": current_user.email,
        "username": current_user.username
    }