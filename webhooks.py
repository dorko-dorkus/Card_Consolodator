from flask import Blueprint, request, jsonify
import stripe
import os
from models import db, PlatformGiftCard, User

webhooks_bp = Blueprint('webhooks', __name__)
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@webhooks_bp.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
    """Handles Stripe webhook events and updates the system accordingly."""
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid signature"}), 400
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        user_id = int(payment_intent['metadata']['user_id'])
        amount = payment_intent['amount_received'] / 100
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 400
        
        # Update user's platform gift card balance
        platform_card = PlatformGiftCard.query.filter_by(user_id=user_id).first()
        if platform_card:
            platform_card.balance += amount
        else:
            platform_card = PlatformGiftCard(user_id=user_id, balance=amount)
            db.session.add(platform_card)
        
        db.session.commit()
        print(f"Payment succeeded for User {user_id}: ${amount}. Updated balance: ${platform_card.balance}")
    
    elif event['type'] == 'issuing_card.created':
        card = event['data']['object']
        print(f"New virtual card issued: {card['id']}")
    
    return jsonify({"status": "success"}), 200
