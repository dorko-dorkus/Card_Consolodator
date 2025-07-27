import os

os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test")

from app.__init__ import create_app, db, bcrypt
from app.models import User, PlatformGiftCard, Transaction


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


def test_purchase_success(mocker):
    app = setup_app()
    user_id = create_user(app)
    client = app.test_client()

    with app.app_context():
        card = PlatformGiftCard(user_id=user_id, balance=20, stripe_card_id="pm_123")
        db.session.add(card)
        db.session.commit()

    mocker.patch("app.routes.stripe.PaymentIntent.create", return_value=type('obj', (object,), {'id': 'pi_789'})())

    resp = client.post('/api/purchase', json={'user_id': user_id, 'amount': 15})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['remaining_balance'] == 5

    with app.app_context():
        platform = PlatformGiftCard.query.filter_by(user_id=user_id).first()
        assert platform.balance == 5
        txns = Transaction.query.filter_by(user_id=user_id).all()
        assert len(txns) == 1
        assert txns[0].stripe_payment_id == 'pi_789'
        assert txns[0].transaction_type == 'Purchase'


def test_purchase_insufficient_balance():
    app = setup_app()
    user_id = create_user(app)
    client = app.test_client()

    with app.app_context():
        card = PlatformGiftCard(user_id=user_id, balance=5)
        db.session.add(card)
        db.session.commit()

    resp = client.post('/api/purchase', json={'user_id': user_id, 'amount': 10})
    assert resp.status_code == 400
    assert 'error' in resp.get_json()

