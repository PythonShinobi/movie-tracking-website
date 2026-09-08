import secrets
import hashlib


class EmailVerificationTokenService:
    """Generate secure email verification tokens."""

    def generate_token_and_hash(self) -> tuple[str, str]:
        """Return the raw token and its hash."""

        raw_token = secrets.token_urlsafe(32)
        
        token_hash = hashlib.sha256(
            raw_token.encode("utf-8")
        ).hexdigest()

        return raw_token, token_hash