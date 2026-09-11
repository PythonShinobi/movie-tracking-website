import secrets
import hashlib
from datetime import (
    datetime,
    timedelta,
    timezone
)

from app.domain.email_verification_token import EmailVerificationToken


class EmailVerificationTokenService:
    """Generate secure email verification tokens."""

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