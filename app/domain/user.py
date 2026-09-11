"""Domain model representing a user of the movie tracking application."""

class User:
    """Represent a user in the movie tracking system."""

    def __init__(
            self,
            id: int | None,
            email: str,
            username: str,
            password_hash: str,
            email_verified: bool = False
    ) -> None:
        self.id = id
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.email_verified = email_verified


    def change_password(self, password_hash: str) -> None:
        """Replace the user's current password hash."""

        self.password_hash = password_hash


    def verify_email(self) -> None:
        """Set domain object email_verified state to True."""
        
        self.email_verified = True