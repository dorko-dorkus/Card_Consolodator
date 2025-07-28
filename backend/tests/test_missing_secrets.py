import os
import importlib
import pytest


def reload_modules():
    import app.config
    import app.__init__
    importlib.reload(app.config)
    importlib.reload(app.__init__)
    return app.__init__


@pytest.mark.parametrize("missing_key", [
    "SECRET_KEY",
    "STRIPE_SECRET_KEY",
    "STRIPE_PUBLISHABLE_KEY",
    "STRIPE_WEBHOOK_SECRET",
])
def test_create_app_fails_without_required_env(monkeypatch, missing_key):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    # provide valid values for all keys then remove one
    monkeypatch.setenv("SECRET_KEY", "v")
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk")
    monkeypatch.setenv("STRIPE_PUBLISHABLE_KEY", "pk")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "wh")
    monkeypatch.delenv(missing_key, raising=False)

    with pytest.raises(RuntimeError):
        modules = reload_modules()
        modules.create_app()
