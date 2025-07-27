import os
import pytest

os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test")

from app.__init__ import create_app, db, bcrypt
from app.models import User


def setup_app():
    app = create_app()
    with app.app_context():
        db.create_all()
    return app


def test_register_and_login():
    app = setup_app()
    client = app.test_client()

    resp = client.post('/api/register', json={
        'name': 'Test',
        'email': 'test@example.com',
        'password': 'secret'
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['message'] == 'registered'

    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert bcrypt.check_password_hash(user.password_hash, 'secret')

    client.post('/api/logout')

    resp = client.post('/api/login', json={'email': 'test@example.com', 'password': 'secret'})
    assert resp.status_code == 200
    assert resp.get_json()['message'] == 'logged in'

    resp = client.get('/api/session')
    assert resp.get_json()['authenticated'] is True


def test_login_failure():
    app = setup_app()
    with app.app_context():
        pw = bcrypt.generate_password_hash('pw').decode('utf-8')
        user = User(name='User', email='user@example.com', password_hash=pw)
        db.session.add(user)
        db.session.commit()

    client = app.test_client()
    resp = client.post('/api/login', json={'email': 'user@example.com', 'password': 'wrong'})
    assert resp.status_code == 401
