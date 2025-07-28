import os

os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test")
os.environ.setdefault("STRIPE_PUBLISHABLE_KEY", "pk_test")
os.environ.setdefault("STRIPE_WEBHOOK_SECRET", "whsec_test")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test")
os.environ.setdefault("CORS_ORIGINS", "http://localhost")

from app.__init__ import create_app, db, bcrypt
from datetime import datetime
from app.models import User, GiftCard


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
        card = GiftCard(
            user_id=user.user_id,
            token="tok",
            expiry_date=datetime(2099, 1, 1),
            source="physical",
        )
        db.session.add(card)
        db.session.commit()
        return user.user_id


def test_delete_account():
    app = setup_app()
    user_id = create_user(app)
    client = app.test_client()
    client.post("/api/login", json={"email": "u@example.com", "password": "pw"})

    resp = client.delete(f"/api/users/{user_id}")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "account deleted"

    with app.app_context():
        assert db.session.get(User, user_id) is None
        assert GiftCard.query.filter_by(user_id=user_id).count() == 0


def test_delete_account_wrong_user():
    app = setup_app()
    user_id = create_user(app)
    with app.app_context():
        pw = bcrypt.generate_password_hash("pw2").decode("utf-8")
        other = User(name="O", email="o@example.com", password_hash=pw)
        db.session.add(other)
        db.session.commit()
        other_id = other.user_id
    client = app.test_client()
    client.post("/api/login", json={"email": "o@example.com", "password": "pw2"})
    resp = client.delete(f"/api/users/{user_id}")
    assert resp.status_code == 403
    with app.app_context():
        assert db.session.get(User, user_id) is not None
        assert db.session.get(User, other_id) is not None


def test_delete_requires_login():
    app = setup_app()
    user_id = create_user(app)
    client = app.test_client()
    resp = client.delete(f"/api/users/{user_id}")
    assert resp.status_code == 302
