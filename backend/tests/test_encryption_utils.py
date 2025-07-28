import importlib
import sys


def test_generated_key_permissions(tmp_path, monkeypatch):
    key_path = tmp_path / "enc.key"
    monkeypatch.setenv("ENCRYPTION_KEY_PATH", str(key_path))
    monkeypatch.delenv("ENCRYPTION_KEY", raising=False)

    sys.modules.pop("app.encryption_utils", None)
    eu = importlib.import_module("app.encryption_utils")
    importlib.reload(eu)

    assert key_path.exists()
    mode = key_path.stat().st_mode & 0o777
    assert mode == 0o600
