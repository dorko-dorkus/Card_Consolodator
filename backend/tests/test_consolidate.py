import os
from datetime import datetime

os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test")

from app.__init__ import create_app, db, bcrypt
from app.models import User, GiftCard, PlatformGiftCard
from app.routes import encrypt_data


def setup_app():
    app = create_app()
    with app.app_context():
        db.create_all()
    return app


def create_user_with_cards(app):
    with app.app_context():
        pw = bcrypt.generate_password_hash('pw').decode('utf-8')
        user = User(name='U', email='u@example.com', password_hash=pw)
        db.session.add(user)
        db.session.commit()
        gc1 = GiftCard(user_id=user.user_id, card_number=encrypt_data('111111111111'),
                       balance=10, expiry_date=datetime(2099,1,1), is_active=True,
                       source='physical_card')
        gc2 = GiftCard(user_id=user.user_id, card_number=encrypt_data('222222222222'),
                       balance=20, expiry_date=datetime(2099,1,1), is_active=True,
                       source='physical_card')
        db.session.add_all([gc1, gc2])
        db.session.commit()
        return user.user_id


def test_consolidate_cards(mocker):
    app = setup_app()
    user_id = create_user_with_cards(app)
    client = app.test_client()
    client.post('/api/login', json={'email': 'u@example.com', 'password': 'pw'})

    mocker.patch('app.routes.stripe.PaymentIntent.create', return_value=type('obj',(object,),{'client_secret':'secret'})())

    resp = client.post('/api/consolidate', json={'user_id': user_id})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['message'] == 'Consolidation complete'
    assert data['client_secret'] == 'secret'

    with app.app_context():
        platform = PlatformGiftCard.query.filter_by(user_id=user_id).first()
        assert platform is not None
        assert platform.balance == 30
        cards = GiftCard.query.filter_by(user_id=user_id).all()
        assert all(card.balance == 0 for card in cards)
        assert all(card.is_active is False for card in cards)


def test_consolidate_requires_login(mocker):
    app = setup_app()
    user_id = create_user_with_cards(app)
    client = app.test_client()
    mocker.patch('app.routes.stripe.PaymentIntent.create', return_value=type('obj',(object,),{'client_secret':'secret'})())
    resp = client.post('/api/consolidate', json={'user_id': user_id})
    assert resp.status_code == 302

