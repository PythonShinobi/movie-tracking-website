"""Domain model representing email verification tokens.

This module defines the EmailVerificationToken domain object used to
represent the state of a token issued when a user needs to verify their
email address.

The domain object stores the token's ownership, hashed value, expiration
time, and usage state. It also contains the business behavior for
determining whether a token has expired, determining whether it has
already been used, and marking it as used after successful verification.

The domain model does not depend on the database, email system, or Flask.
"""


from datetime import datetime


class EmailVerificationToken:
    """Represent a token used to verify a user's email address.

    The token tracks which user it belongs to, when it expires, and
    whether it has already been used.
    """

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
        """Return True when the token is expired."""

        return now >= self.expires_at

    def is_used(self) -> bool:
        """Return True when the token has already been used."""

        return self.used_at is not None

    def mark_used(self, now: datetime) -> None:
        """Mark the token as used."""
        
        self.used_at = now