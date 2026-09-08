import hashlib

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