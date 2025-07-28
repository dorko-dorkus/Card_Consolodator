from datetime import datetime
from flask_login import UserMixin
from .__init__ import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    stripe_customer_id = db.Column(db.String, unique=True, nullable=True)  # Stripe Customer ID

    gift_cards = db.relationship("GiftCard", back_populates="user")
    platform_cards = db.relationship("PlatformGiftCard", back_populates="user")
    transactions = db.relationship("Transaction", back_populates="user")
    bank_accounts = db.relationship("BankAccount", back_populates="user")

    def get_id(self):
        """Return the user identifier for Flask-Login sessions."""
        return str(self.user_id)

class GiftCard(db.Model):
    __tablename__ = 'gift_cards'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    token = db.Column(db.String, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    source = db.Column(db.String, nullable=False)  # e.g., "physical_card", "bank_transfer"

    user = db.relationship("User", back_populates="gift_cards")

class PlatformGiftCard(db.Model):
    __tablename__ = 'platform_gift_cards'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    stripe_card_id = db.Column(db.String, unique=True, nullable=True)  # Stripe-issued NFC card ID

    user = db.relationship("User", back_populates="platform_cards")

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    transaction_type = db.Column(db.String, nullable=False)  # Deposit, Transfer, Consolidation
    amount = db.Column(db.Float, nullable=False)
    stripe_payment_id = db.Column(db.String, unique=True, nullable=True)  # Stripe Payment Intent ID
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="transactions")


class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    stripe_bank_account_id = db.Column(db.String, unique=True, nullable=False)
    bank_name = db.Column(db.String, nullable=True)
    last4 = db.Column(db.String, nullable=True)

    user = db.relationship("User", back_populates="bank_accounts")
