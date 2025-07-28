import os

os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test")
os.environ.setdefault("AML_THRESHOLD", "5000")

from app.__init__ import create_app, db, bcrypt
from app.models import User
from app import aml


def setup_app():
    app = create_app()
    with app.app_context():
        db.create_all()
    return app


def create_user(app):
    with app.app_context():
        pw = bcrypt.generate_password_hash("pw").decode("utf-8")
        user = User(name="U", email="u@example.com", password_hash=pw)
        db.session.add(user)
        db.session.commit()
        return user.user_id


def test_large_purchase_triggers_report(mocker, tmp_path):
    log_path = tmp_path / "smr.log"
    os.environ["ENABLE_LIVE_SUBMISSION"] = "false"
    aml.LOCAL_SM_LOG_PATH = str(log_path)
    aml.ENABLE_LIVE_SUBMISSION = False

    app = setup_app()
    user_id = create_user(app)
    client = app.test_client()
    client.post("/api/login", json={"email": "u@example.com", "password": "pw"})

    spy = mocker.spy(aml, "report_suspicious_activity")
    review_spy = mocker.spy(aml, "manual_review")
    post_mock = mocker.patch("requests.post")

    mocker.patch("app.routes.stripe.PaymentIntent.create", return_value=type("obj", (object,), {"id": "pi_lg"})())

    resp = client.post(
        "/api/purchase",
        json={"user_id": user_id, "amount": 6000, "payment_token": "pm_card"},
    )
    assert resp.status_code == 200
    assert spy.call_count == 1
    post_mock.assert_not_called()
    review_spy.assert_called()
    with open(log_path) as f:
        lines = f.readlines()
        assert len(lines) >= 1
        import json
        report = json.loads(lines[-1])
        assert report["reason"] == "Amount exceeds threshold"
