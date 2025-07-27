from cryptography.fernet import Fernet
import os
import stripe
from flask import Blueprint, request, jsonify
from datetime import datetime

from .models import db, GiftCard, PlatformGiftCard, User

# Load encryption key from environment variable or file
ENCRYPTION_KEY_PATH = os.getenv("ENCRYPTION_KEY_PATH", "encryption_key.key")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY

def load_encryption_key():
    if os.getenv("ENCRYPTION_KEY"):  # Load from environment variable if available
        return os.getenv("ENCRYPTION_KEY").encode()

    if os.path.exists(ENCRYPTION_KEY_PATH):
        with open(ENCRYPTION_KEY_PATH, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_PATH, "wb") as key_file:
            key_file.write(key)
        return key

encryption_key = load_encryption_key()
cipher = Fernet(encryption_key)

def encrypt_data(data):
    """Encrypts a string using Fernet encryption."""
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    """Decrypts a string using Fernet encryption."""
    try:
        return cipher.decrypt(encrypted_data.encode()).decode()
    except Exception:
        return "Decryption error: Invalid or corrupted data"

def create_payment_intent(amount, currency="usd"):
    """Creates a Stripe Payment Intent for consolidating gift cards."""
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Stripe uses cents
            currency=currency,
            payment_method_types=["card"],
        )
        return intent.client_secret
    except stripe.error.StripeError as e:
        return f"Stripe error: {str(e)}"

def verify_payment(payment_intent_id):
    """Verifies a Stripe Payment Intent status."""
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return intent.status == "succeeded"
    except stripe.error.StripeError:
        return False


# Blueprint exposing REST API endpoints
api_bp = Blueprint("api", __name__)


@api_bp.route("/gift-cards", methods=["GET"])
def get_gift_cards():
    """Return all gift cards for the specified user."""
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    cards = GiftCard.query.filter_by(user_id=user_id).all()
    result = []
    for card in cards:
        result.append({
            "card_id": card.card_id,
            "card_number": decrypt_data(card.card_number),
            "balance": card.balance,
            "expiry_date": card.expiry_date.isoformat()
            if isinstance(card.expiry_date, datetime)
            else str(card.expiry_date),
            "is_active": card.is_active,
            "source": card.source,
        })
    return jsonify(result)


@api_bp.route("/consolidate", methods=["POST"])
def consolidate_cards():
    """Consolidate all active gift cards into the user's platform card."""
    data = request.get_json() or {}
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    cards = GiftCard.query.filter_by(user_id=user_id, is_active=True).all()
    if not cards:
        return jsonify({"message": "No gift cards to consolidate."})

    total = sum(card.balance for card in cards)
    for card in cards:
        card.is_active = False
        card.balance = 0

    platform_card = PlatformGiftCard.query.filter_by(user_id=user_id).first()
    if platform_card:
        platform_card.balance += total
    else:
        platform_card = PlatformGiftCard(user_id=user_id, balance=total)
        db.session.add(platform_card)

    db.session.commit()

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),
            currency="usd",
            metadata={"user_id": user_id},
        )
        client_secret = intent.client_secret
    except stripe.error.StripeError:
        client_secret = None

    return jsonify({"message": "Consolidation complete", "client_secret": client_secret})
