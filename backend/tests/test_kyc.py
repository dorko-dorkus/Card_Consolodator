import os

os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test")
os.environ.setdefault("STRIPE_PUBLISHABLE_KEY", "pk_test")
os.environ.setdefault("STRIPE_WEBHOOK_SECRET", "whsec_test")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test")
os.environ.setdefault("CORS_ORIGINS", "http://localhost")

from app.__init__ import create_app, db, bcrypt
from app.models import User, UserProfile
from app import aml, kyc


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


def test_daily_limit_triggers_kyc(mocker):
    app = setup_app()
    user_id = create_user(app)
    mocker.patch("app.kyc.create_verification_session", return_value="sess")
    with app.app_context():
        for _ in range(4):
            aml.log_transaction(user_id, 250, "purchase")
        profile = kyc.get_user_profile(user_id)
        assert profile.kyc_status == "pending"
        db_profile = db.session.get(UserProfile, user_id)
        assert db_profile.verification_status == "pending"


def test_single_large_transaction_flagged(mocker):
    app = setup_app()
    user_id = create_user(app)
    mocker.patch("app.kyc.create_verification_session", return_value="sess")
    with app.app_context():
        aml.log_transaction(user_id, 350, "purchase")
        profile = kyc.get_user_profile(user_id)
        assert profile.flagged is True
        assert db.session.get(UserProfile, user_id).flagged is True


def test_transaction_totals_persist():
    app = setup_app()
    user_id = create_user(app)
    with app.app_context():
        aml.log_transaction(user_id, 100, "purchase")
        aml.log_transaction(user_id, 50, "purchase")
        profile = kyc.get_user_profile(user_id)
        assert profile.daily_total == 150
        assert profile.weekly_total == 150
        # ensure fetching again reflects stored totals
        profile2 = kyc.get_user_profile(user_id)
        assert profile2.daily_total == 150
        db_profile = db.session.get(UserProfile, user_id)
        assert db_profile.daily_total == 150
        assert db_profile.weekly_total == 150


def test_card_balances_persist():
    app = setup_app()
    user_id = create_user(app)
    with app.app_context():
        profile = kyc.get_user_profile(user_id)
        kyc.update_card_balance(profile, 1, 20.0)
        profile2 = kyc.get_user_profile(user_id)
        assert profile2.card_balances == [(1, 20.0)]
