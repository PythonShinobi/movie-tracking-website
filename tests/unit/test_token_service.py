import hashlib
from datetime import datetime, timezone

from app.services.token import EmailVerificationTokenService


def test_generate_token_and_hash_returns_token_and_hash():
    service = EmailVerificationTokenService()

    raw_token, token_hash = service.generate_token_and_hash()

    expected_hash = hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()

    assert raw_token
    assert token_hash == expected_hash


def test_generate_token_and_hash_returns_unique_tokens():
    service = EmailVerificationTokenService()

    raw_token_1, _ = service.generate_token_and_hash()
    raw_token_2, _ = service.generate_token_and_hash()

    assert raw_token_1 != raw_token_2


def test_create_verification_token_assigns_user_id():
    service = EmailVerificationTokenService()

    token, raw_token = service.create_verification_token(user_id=123)

    assert token.user_id == 123
    assert  raw_token


def test_create_verification_token_stores_hash_and_not_raw_token():
    service = EmailVerificationTokenService()

    token, raw_token = service.create_verification_token(user_id=123)

    expected_hash = hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()

    assert token.random_token_hash == expected_hash
    assert token.random_token_hash != raw_token


def test_create_verification_token_has_expiration():
    service = EmailVerificationTokenService()

    token, _ = service.create_verification_token(user_id=123)

    now = datetime.now(timezone.utc)

    assert token.expires_at > now