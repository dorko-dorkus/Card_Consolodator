import os
import re
import stripe
from flask import Blueprint, request, jsonify, current_app
from flask_limiter.errors import RateLimitExceeded
from flask_login import login_user, logout_user, current_user, login_required
from .__init__ import bcrypt, csrf
from .aml import log_transaction
from .stripeUtils import issue_virtual_card
from datetime import datetime
from .config import Config

from .models import (
    db,
    GiftCard,
    PlatformGiftCard,
    User,
    BankAccount,
    Transaction,
)

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", Config.STRIPE_SECRET_KEY)
stripe.api_key = STRIPE_SECRET_KEY

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


def validate_card_details(card_number: str, expiry_date: str):
    """Validate card number format and expiry date."""
    if not re.fullmatch(r"\d{12,19}", str(card_number)):
        return "Invalid card number"
    try:
        exp = datetime.strptime(expiry_date, "%Y-%m-%d")
    except ValueError:
        return "Invalid expiry date format"
    if exp.date() < datetime.utcnow().date():
        return "Card already expired"
    return None


# Blueprint exposing REST API endpoints
api_bp = Blueprint("api", __name__)


@api_bp.errorhandler(Exception)
def handle_exception(error):
    from flask import current_app
    if isinstance(error, RateLimitExceeded):
        return jsonify({"error": "Rate limit exceeded"}), 429
    current_app.logger.exception("Unhandled exception")
    db.session.rollback()
    return jsonify({"error": "Server error"}), 500

EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")


@csrf.exempt
@api_bp.route("/register", methods=["POST"])
def register():
    """Register a new user and log them in."""
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not all([name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400
    if not EMAIL_RE.fullmatch(email):
        return jsonify({"error": "Invalid email"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password too short"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(name=name, email=email, password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return jsonify({"message": "registered", "user_id": user.user_id})


@csrf.exempt
@api_bp.route("/login", methods=["POST"])
def login():
    """Authenticate an existing user."""
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not all([email, password]):
        return jsonify({"error": "Missing credentials"}), 400
    if not EMAIL_RE.fullmatch(email):
        return jsonify({"error": "Invalid email"}), 400

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({"message": "logged in"})
    return jsonify({"error": "Invalid credentials"}), 401


@api_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    return jsonify({"message": "logged out"})


@api_bp.route("/session", methods=["GET"])
def session_info():
    """Return session status for the current user."""
    if current_user.is_authenticated:
        return jsonify({"authenticated": True, "user_id": current_user.user_id})
    return jsonify({"authenticated": False})


@api_bp.route("/gift-cards", methods=["GET"])
@login_required
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
            "card_token": card.token,
            "expiry_date": card.expiry_date.isoformat()
            if isinstance(card.expiry_date, datetime)
            else str(card.expiry_date),
            "is_active": card.is_active,
            "source": card.source,
        })
    return jsonify(result)


@api_bp.route("/gift-cards", methods=["POST"])
@login_required
def add_gift_card():
    """Add a new gift card for a user."""
    data = request.get_json() or {}
    user_id = data.get("user_id")
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid user_id"}), 400
    card_token = data.get("card_token")
    expiry = data.get("expiry_date")
    source = data.get("source", "physical_card")

    if not all([user_id, card_token, expiry]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        exp_dt = datetime.strptime(expiry, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid expiry date format"}), 400
    if exp_dt.date() < datetime.utcnow().date():
        return jsonify({"error": "Card already expired"}), 400

    existing = GiftCard.query.filter_by(user_id=user_id, token=card_token).first()
    if existing:
        return jsonify({"error": "Card already exists"}), 409

    new_card = GiftCard(
        user_id=user_id,
        token=card_token,
        expiry_date=exp_dt,
        source=source,
    )
    db.session.add(new_card)
    db.session.commit()
    return jsonify({"message": "card added", "card_id": new_card.card_id}), 201


@api_bp.route("/consolidate", methods=["POST"])
@login_required
def consolidate_cards():
    """Consolidate a user's gift cards onto a platform card."""
    data = request.get_json() or {}
    user_id = data.get("user_id")
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid user_id"}), 400
    if user_id != current_user.user_id:
        return jsonify({"error": "forbidden"}), 403

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    cards = GiftCard.query.filter_by(user_id=user_id, is_active=True).all()
    if not cards:
        return jsonify({"error": "No active cards"}), 400

    platform_card = PlatformGiftCard.query.filter_by(user_id=user_id).first()
    if not platform_card:
        try:
            virt = issue_virtual_card(user.name, user.email)
            platform_card = PlatformGiftCard(
                user_id=user_id, stripe_card_id=getattr(virt, "id", None)
            )
            db.session.add(platform_card)
        except Exception as e:  # pragma: no cover - stripe failure
            return jsonify({"error": str(e)}), 400

    for card in cards:
        card.is_active = False

    db.session.commit()
    log_transaction(user_id=user_id, amount=0.0, transaction_type="consolidate")

    return jsonify(
        {
            "message": "consolidation complete",
            "platform_card_id": platform_card.card_id,
            "deactivated": len(cards),
        }
    )



@api_bp.route("/bank-accounts/link", methods=["POST"])
@login_required
def link_bank_account():
    """Link a user's bank account via Stripe ACH."""
    data = request.get_json() or {}
    user_id = data.get("user_id")
    bank_token = data.get("bank_token")
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid user_id"}), 400

    if not all([user_id, bank_token]):
        return jsonify({"error": "user_id and bank_token required"}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.stripe_customer_id:
        try:
            customer = stripe.Customer.create(email=user.email, name=user.name)
            user.stripe_customer_id = customer.id
            db.session.commit()
        except stripe.error.StripeError as e:
            return jsonify({"error": str(e)}), 400

    try:
        bank_account = stripe.Customer.create_source(
            user.stripe_customer_id,
            source=bank_token,
        )
    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400

    new_account = BankAccount(
        user_id=user_id,
        stripe_bank_account_id=bank_account.id,
        bank_name=getattr(bank_account, "bank_name", None),
        last4=getattr(bank_account, "last4", None),
    )
    db.session.add(new_account)
    db.session.commit()

    return jsonify({"message": "bank account linked", "account_id": new_account.account_id})



@api_bp.route("/purchase", methods=["POST"])
@login_required
def make_purchase():
    """Charge a user's payment token for a purchase."""

    data = request.get_json() or {}
    user_id = data.get("user_id")
    amount = data.get("amount")
    payment_token = data.get("payment_token")

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid user_id"}), 400

    if user_id is None or amount is None or not payment_token:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid amount"}), 400

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency="usd",
            payment_method=payment_token,
            confirm=True,
        )
        stripe_id = intent.id
    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400

    current_app.logger.info(
        "purchase", extra={"user_id": user_id, "stripe_payment_id": stripe_id, "timestamp": datetime.utcnow().isoformat()}
    )

    log_transaction(user_id=user_id, amount=amount, transaction_type="purchase", stripe_payment_id=stripe_id)

    return jsonify({"message": "purchase successful"})


@api_bp.route("/users/<int:user_id>", methods=["DELETE"])
@login_required
def delete_account(user_id):
    """Delete the authenticated user's account and related data."""
    if user_id != current_user.user_id:
        return jsonify({"error": "forbidden"}), 403

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    GiftCard.query.filter_by(user_id=user_id).delete()
    PlatformGiftCard.query.filter_by(user_id=user_id).delete()
    BankAccount.query.filter_by(user_id=user_id).delete()
    Transaction.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return jsonify({"message": "account deleted"})
