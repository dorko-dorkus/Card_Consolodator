import os
import pytest

os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test")

from app.__init__ import create_app, db, bcrypt
from app.models import User, GiftCard


def setup_app():
    app = create_app()
    with app.app_context():
        db.create_all()
    return app


def create_user(app):
    with app.app_context():
        pw = bcrypt.generate_password_hash('pw').decode('utf-8')
        user = User(name='U', email='u@example.com', password_hash=pw)
        db.session.add(user)
        db.session.commit()
        return user.user_id


def test_add_gift_card_success():
    app = setup_app()
    user_id = create_user(app)
    client = app.test_client()
    client.post('/api/login', json={'email': 'u@example.com', 'password': 'pw'})

    resp = client.post('/api/gift-cards', json={
        'user_id': user_id,
        'card_token': 'tok_123456',
        'balance': 25,
        'expiry_date': '2099-01-01',
        'source': 'physical_card'
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['message'] == 'card added'

    with app.app_context():
        cards = GiftCard.query.filter_by(user_id=user_id).all()
        assert len(cards) == 1
        assert cards[0].balance == 25
        assert cards[0].token == 'tok_123456'


def test_add_gift_card_expired():
    app = setup_app()
    user_id = create_user(app)
    client = app.test_client()
    client.post('/api/login', json={'email': 'u@example.com', 'password': 'pw'})

    resp = client.post('/api/gift-cards', json={
        'user_id': user_id,
        'card_token': 'tok_expired',
        'balance': 10,
        'expiry_date': '2000-01-01'
    })
    assert resp.status_code == 400
    assert 'error' in resp.get_json()


def test_get_cards_requires_login():
    app = setup_app()
    user_id = create_user(app)
    client = app.test_client()
    resp = client.get(f'/api/gift-cards?user_id={user_id}')
    assert resp.status_code == 302

