"""Password hashing and verification using bcrypt."""

import bcrypt

class PasswordHasher:
    """Hash and verify user passwords using bcrypt."""

    def hash(self, password: str) -> str:
        """Hash a plaintext password."""

        # Encode because bcrypt operates on bytes.
        password_bytes = password.encode("utf-8")
        
        # Generate a random salt.
        salt = bcrypt.gensalt()

        # Produce the password hash.
        password_hash = bcrypt.hashpw(password_bytes, salt)

        # Turn bytes back into a string so it can be stored
        # in the database.
        return password_hash.decode("utf-8")

    def verify(
        self,
        password: str,
        password_hash: str
    ) -> bool:
        """Verify a plaintext password against a stored hash."""

        password_bytes = password.encode("utf-8")  # Encode because bcrypt operates on bytes.
        password_hash_bytes = password_hash.encode("utf-8")  # Encode because bcrypt operates on bytes.

        return bcrypt.checkpw(password_bytes, password_hash_bytes)