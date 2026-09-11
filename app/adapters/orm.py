"""Map domain models to database tables using SQLAlchemy.

This module defines the ORM models used to represent domain data in the
database. It keeps database-specific persistence concerns separate from
the domain models.

Examples:
    - UserModelRecord: Maps User domain data to the users database table.
    - SQLAlchemy columns: Define how attributes such as user IDs, email
      addresses, usernames, and password hashes are stored.
    - ORM relationships: Define associations between persisted models when
      the application requires related database records.
"""

from app.extensions import db


class UserModelRecord(db.Model):
    """Represent a user record in the database.

    This ORM model maps the User domain object to the database and defines
    how user data is stored and retrieved through SQLAlchemy.

    Examples:
        - id: Stores the database-generated user identifier.
        - email: Stores the user's email address.
        - username: Stores the user's username.
        - password_hash: Stores the user's hashed password.
    """

    __tablename__ = "user_model_record"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)


class EmailVerificationTokenModelRecord(db.Model):
    """Represent an email verification token in the database.

    This SQLAlchemy model represents the database record used to persist
    email verification tokens. It belongs to the infrastructure layer and
    is separate from the EmailVerificationToken domain object.
    """

    __tablename__ = "email_verification_token_record"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey("user_model_record.id"),
        nullable=False
    )

    token_hash = db.Column(
        db.String(64),
        unique=True,
        nullable=False
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    used_at = db.Column(
        db.DateTime,
        nullable=True
    )