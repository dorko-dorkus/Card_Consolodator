import os
import pytest

os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test")
os.environ.setdefault("STRIPE_PUBLISHABLE_KEY", "pk_test")
os.environ.setdefault("STRIPE_WEBHOOK_SECRET", "whsec_test")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test")
os.environ.setdefault("RATE_LIMIT", "1/minute")

from app.__init__ import create_app, db, bcrypt, limiter
from app.models import User


def setup_app():
    app = create_app()
    with app.app_context():
        db.create_all()
    limiter.reset()
    return app


def create_user(app):
    with app.app_context():
        pw = bcrypt.generate_password_hash('pw').decode('utf-8')
        user = User(name='U', email='u@example.com', password_hash=pw)
        db.session.add(user)
        db.session.commit()
        return user.user_id


def test_unhandled_exception_returns_500(mocker):
    app = setup_app()
    user_id = create_user(app)
    client = app.test_client()
    client.post('/api/login', json={'email': 'u@example.com', 'password': 'pw'})

    mocker.patch('app.routes.stripe.PaymentIntent.create', side_effect=Exception('boom'))
    resp = client.post('/api/purchase', json={'user_id': user_id, 'amount': 5, 'payment_token': 'pm_card'})
    assert resp.status_code == 500
    assert resp.get_json()['error'] == 'Server error'


def test_rate_limit_headers():
    app = setup_app()
    client = app.test_client()

    resp1 = client.get('/api/session')
    assert resp1.status_code == 200

    resp2 = client.get('/api/session')
    assert resp2.status_code == 429
    assert 'Retry-After' in resp2.headers
    assert resp2.headers.get('X-RateLimit-Remaining') == '0'

