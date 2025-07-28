import os
import pytest

os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test")
os.environ.setdefault("STRIPE_PUBLISHABLE_KEY", "pk_test")
os.environ.setdefault("STRIPE_WEBHOOK_SECRET", "whsec_test")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test")

from app.__init__ import create_app, db, bcrypt
from app.models import User, BankAccount


def setup_app():
    app = create_app()
    with app.app_context():
        db.create_all()
    return app


def create_user(app, with_customer=False):
    with app.app_context():
        pw = bcrypt.generate_password_hash('pw').decode('utf-8')
        user = User(name='U', email='u@example.com', password_hash=pw)
        if with_customer:
            user.stripe_customer_id = 'cus_123'
        db.session.add(user)
        db.session.commit()
        return user.user_id


def test_link_bank_account(mocker):
    app = setup_app()
    user_id = create_user(app)
    client = app.test_client()
    client.post('/api/login', json={'email': 'u@example.com', 'password': 'pw'})

    mocker.patch("app.routes.stripe.Customer.create", return_value=type('obj', (object,), {'id': 'cus_123'})())
    mocker.patch("app.routes.stripe.Customer.create_source", return_value=type('obj', (object,), {'id': 'ba_123', 'bank_name': 'Bank', 'last4': '1234'})())

    resp = client.post('/api/bank-accounts/link', json={'user_id': user_id, 'bank_token': 'tok_bank'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['message'] == 'bank account linked'

    with app.app_context():
        accounts = BankAccount.query.filter_by(user_id=user_id).all()
        assert len(accounts) == 1
        assert accounts[0].stripe_bank_account_id == 'ba_123'




def test_link_bank_account_requires_login(mocker):
    app = setup_app()
    user_id = create_user(app)
    client = app.test_client()
    mocker.patch("app.routes.stripe.Customer.create", return_value=type('obj', (object,), {'id': 'cus_123'})())
    mocker.patch("app.routes.stripe.Customer.create_source", return_value=type('obj', (object,), {'id': 'ba_123', 'bank_name': 'Bank', 'last4': '1234'})())
    resp = client.post('/api/bank-accounts/link', json={'user_id': user_id, 'bank_token': 'tok_bank'})
    assert resp.status_code == 302


