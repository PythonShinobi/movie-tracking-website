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

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)