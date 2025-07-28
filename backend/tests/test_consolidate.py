import os
from datetime import datetime

os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test")
os.environ.setdefault("STRIPE_PUBLISHABLE_KEY", "pk_test")
os.environ.setdefault("STRIPE_WEBHOOK_SECRET", "whsec_test")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test")

from app.__init__ import create_app, db, bcrypt
from app.models import User, GiftCard, PlatformGiftCard


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


def test_consolidate_cards(mocker):
    app = setup_app()
    user_id = create_user(app)
    with app.app_context():
        card1 = GiftCard(user_id=user_id, token="tok1", expiry_date=datetime(2099,1,1), source="physical")
        card2 = GiftCard(user_id=user_id, token="tok2", expiry_date=datetime(2099,1,1), source="physical")
        db.session.add_all([card1, card2])
        db.session.commit()

    client = app.test_client()
    client.post('/api/login', json={'email': 'u@example.com', 'password': 'pw'})

    mocker.patch('app.routes.issue_virtual_card', return_value=type('obj',(object,),{'id':'pc_123'})())

    resp = client.post('/api/consolidate', json={'user_id': user_id})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['message'] == 'consolidation complete'

    with app.app_context():
        cards = GiftCard.query.filter_by(user_id=user_id).all()
        assert all(not c.is_active for c in cards)
        assert PlatformGiftCard.query.filter_by(user_id=user_id).count() == 1
