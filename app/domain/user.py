"""Domain model representing a user of the movie tracking application."""

class User:
    """Represent a user in the movie tracking system."""

    def __init__(
            self,
            id: int | None,
            email: str,
            username: str,
            password_hash: str,
    ) -> None:
        self.id = id
        self.email = email
        self.username = username
        self.password_hash = password_hash

    def change_password(self, password_hash: str) -> None:
        """Replace the user's current password hash."""

        self.password_hash = password_hash