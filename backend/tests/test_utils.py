import os
import builtins
import pytest

os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test")

from app.encryption_utils import encrypt_data, decrypt_data
from app.routes import create_payment_intent, verify_payment

class DummyStripeObject:
    def __init__(self, client_secret=None, status="succeeded"):
        self.client_secret = client_secret
        self.status = status


def test_encrypt_decrypt_roundtrip():
    text = "secret"
    encrypted = encrypt_data(text)
    assert text != encrypted
    decrypted = decrypt_data(encrypted)
    assert decrypted == text


def test_decrypt_invalid_returns_error():
    # not a valid token
    result = decrypt_data("invalid")
    assert result.startswith("Decryption error")


def test_create_payment_intent(mocker):
    mock_create = mocker.patch("app.routes.stripe.PaymentIntent.create",
                               return_value=DummyStripeObject("tok_123"))
    secret = create_payment_intent(10)
    assert secret == "tok_123"
    mock_create.assert_called_once()


def test_verify_payment_success(mocker):
    mock_retrieve = mocker.patch("app.routes.stripe.PaymentIntent.retrieve",
                                return_value=DummyStripeObject(status="succeeded"))
    assert verify_payment("pi_123") is True
    mock_retrieve.assert_called_once_with("pi_123")


def test_verify_payment_failure(mocker):
    mock_retrieve = mocker.patch("app.routes.stripe.PaymentIntent.retrieve",
                                return_value=DummyStripeObject(status="processing"))
    assert verify_payment("pi_456") is False

