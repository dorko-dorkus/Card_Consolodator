import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
import encryption_utils


def test_encrypt_decrypt_roundtrip():
    text = "secret"
    token = encryption_utils.encrypt_data(text)
    assert isinstance(token, str)
    assert encryption_utils.decrypt_data(token) == text


def test_decrypt_invalid():
    assert (
        encryption_utils.decrypt_data("invalid")
        == "Decryption error: Invalid or corrupted data"
    )
