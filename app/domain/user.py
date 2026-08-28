"""Domain model representing a user of the movie tracking application."""

class User:
    """Represent a user in the movie tracking system."""

    def __init__(
            self,
            email: str,
            username: str,
            password_hash: str,
    ) -> None:
        self.email = email
        self.username = username
        self.password_hash = password_hash