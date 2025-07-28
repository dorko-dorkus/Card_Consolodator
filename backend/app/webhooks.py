from flask import Blueprint, request, jsonify
from .__init__ import csrf
import stripe
import os

from .config import Config

webhooks_bp = Blueprint('webhooks', __name__)
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", Config.STRIPE_WEBHOOK_SECRET)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", Config.STRIPE_SECRET_KEY)

@csrf.exempt
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
    except Exception:
        return jsonify({"error": "Webhook error"}), 400
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        user_id = payment_intent['metadata'].get('user_id')
        amount = payment_intent['amount_received'] / 100
        print(f"Payment succeeded for User {user_id}: ${amount}")
    
    elif event['type'] == 'issuing_card.created':
        card = event['data']['object']
        print(f"New virtual card issued: {card['id']}")
    else:
        print(f"Unhandled event type: {event['type']}")

    return jsonify({"status": "success"}), 200
