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
    bank_accounts = db.relationship("BankAccount", back_populates="user")
    transactions = db.relationship("Transaction", back_populates="user")

    def get_id(self):
        """Return the user identifier for Flask-Login sessions."""
        return str(self.user_id)

class GiftCard(db.Model):
    __tablename__ = 'gift_cards'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    token = db.Column(db.String, unique=True, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    source = db.Column(db.String, nullable=False)  # e.g., "physical_card", "bank_transfer"

    user = db.relationship("User", back_populates="gift_cards")

class PlatformGiftCard(db.Model):
    __tablename__ = 'platform_gift_cards'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    stripe_card_id = db.Column(db.String, unique=True, nullable=True)  # Stripe-issued NFC card ID

    user = db.relationship("User", back_populates="platform_cards")


class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    stripe_bank_account_id = db.Column(db.String, unique=True, nullable=False)
    bank_name = db.Column(db.String, nullable=True)
    last4 = db.Column(db.String, nullable=True)

    user = db.relationship("User", back_populates="bank_accounts")


class Transaction(db.Model):
    """Record of payment transactions for AML monitoring."""
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    transaction_type = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    stripe_payment_id = db.Column(db.String, unique=True, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    user = db.relationship("User", back_populates="transactions")

class UserProfile(db.Model):
    """Persistent profile for AML/KYC status."""
    __tablename__ = 'user_profiles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    verification_status = db.Column(db.String, nullable=False, default='not_verified')
    veriff_session_id = db.Column(db.String, nullable=True)
    flagged = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('profile', uselist=False))

    # aliases for backward compatibility
    @property
    def kyc_status(self):
        return self.verification_status

    @kyc_status.setter
    def kyc_status(self, value):
        self.verification_status = value

class IdentificationDocument(db.Model):
    __tablename__ = 'identification_documents'
    doc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.user_id'), nullable=False)
    doc_type = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship('UserProfile', backref='documents')

class VerificationAuditLog(db.Model):
    __tablename__ = 'verification_audit_logs'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.user_id'), nullable=False)
    action = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship('UserProfile', backref='logs')
