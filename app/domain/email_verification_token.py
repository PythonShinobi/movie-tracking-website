from datetime import datetime


class EmailVerificationToken:
    """Represent a token used to verify a user's email address"""

    def __init__(
        self,
        id: int | None,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
        used_at: datetime | None = None
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.token_hash = token_hash
        self.expires_at = expires_at
        self.used_at = used_at

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at

    def is_used(self) -> bool:
        return self.used_at is not None

    def mark_used(self, now: datetime) -> None:
        self.used_at = now