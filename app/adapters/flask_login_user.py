"""Adapt domain users to the interface expected by Flask-Login."""

from app.domain.user import User


class FlaskLoginUser:
    """Adapt a domain User for use with Flask-Login.

    This adapter keeps Flask-Login infrastructure concerns outside
    the domain model while exposing the interface required by
    Flask-Login.

    Examples:
        - is_authenticated: Indicates that the user has been authenticated.
        - is_active: Indicates that the user account is active.
        - is_anonymous: Indicates that the user represents an anonymous user.
        - get_id(): Returns the user's identifier for session storage.
    """

    def __init__(self, user: User) -> None:
        """Initialize the adapter with a domain user."""
        self.user = user

    @property
    def is_authenticated(self) -> bool:
        """Return whether the user is authenticated."""
        return True

    @property
    def is_active(self) -> bool:
        """Return whether the user account is active."""
        return True

    @property
    def is_anonymous(self) -> bool:
        """Return whether the user is anonymous."""
        return False

    def get_id(self) -> str:
        """Return the user's ID as a string."""
        return str(self.user.id)