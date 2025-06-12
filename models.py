from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from flask_login import UserMixin
from app.__init__ import db

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    stripe_customer_id = Column(String, unique=True, nullable=True)  # Stripe Customer ID

    gift_cards = relationship("GiftCard", back_populates="user")
    platform_cards = relationship("PlatformGiftCard", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

class GiftCard(Base):
    __tablename__ = 'gift_cards'
    card_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    card_number = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    source = Column(String, nullable=False)  # e.g., "physical_card", "bank_transfer"

    user = relationship("User", back_populates="gift_cards")

class PlatformGiftCard(Base):
    __tablename__ = 'platform_gift_cards'
    card_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    balance = Column(Float, nullable=False)
    stripe_card_id = Column(String, unique=True, nullable=True)  # Stripe-issued NFC card ID

    user = relationship("User", back_populates="platform_cards")

class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    transaction_type = Column(String, nullable=False)  # Deposit, Transfer, Consolidation
    amount = Column(Float, nullable=False)
    details_encrypted = Column(String, nullable=False)
    stripe_payment_id = Column(String, unique=True, nullable=True)  # Stripe Payment Intent ID
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
