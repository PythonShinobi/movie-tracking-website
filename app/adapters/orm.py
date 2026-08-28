"""Map domain models to database tables using SQLAlchemy."""

from app.extensions import db


class UserModelRecord(db.Model):
    """Represent a user record in the database."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)