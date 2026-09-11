"""Application service for generating email verification tokens.

This module provides the application logic required to create secure
email verification tokens. It generates a cryptographically random raw
token, creates a SHA-256 hash for secure database storage, and creates
an EmailVerificationToken domain object with a fixed expiration time.

The raw token is returned to the application so it can be sent to the
user by email, while only the hashed token is stored in persistent
storage.
"""

import secrets
import hashlib
from datetime import (
    datetime,
    timedelta,
    timezone
)

from app.domain.email_verification_token import EmailVerificationToken


class EmailVerificationTokenService:
    """Generate and prepare secure email verification tokens.

    This service generates cryptographically secure tokens, hashes them
    for storage, and creates EmailVerificationToken domain objects with
    an expiration time.
    """
    
    TOKEN_EXPIRATION_MINUTES = 30

    def generate_token_and_hash(self) -> tuple[str, str]:
        """Generate a cryptographically random token and its hash."""

        # Generate a url safe token value.
        raw_token = secrets.token_urlsafe(32)

        # Encode the raw token to bytes.
        raw_token_bytes = raw_token.encode("utf-8")

        # Generate a hash of the raw token bytes using the sha256 function.
        token_hash = hashlib.sha256(raw_token_bytes).hexdigest()

        return raw_token, token_hash

    def create_verification_token(self, user_id: int) -> tuple[EmailVerificationToken, str]:
        """Create a verification token domain object and
        return its raw token."""

        # Generate a raw token and its hash.
        raw_token, token_hash = self.generate_token_and_hash()

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(minutes=self.TOKEN_EXPIRATION_MINUTES)
        )

        # Create verification token object.
        token = EmailVerificationToken(
            id=None,
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at
        )

        return token, raw_token