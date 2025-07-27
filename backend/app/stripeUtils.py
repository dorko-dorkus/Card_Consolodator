import stripe
import os

# Load Stripe API keys from environment variables
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
stripe.api_key = STRIPE_SECRET_KEY

def create_payment_intent(amount, user_id):
    """Creates a Stripe PaymentIntent for consolidating gift card funds."""
    return stripe.PaymentIntent.create(
        amount=int(amount * 100),  # Convert to cents
        currency="usd",
        description=f"Gift Card Consolidation for User {user_id}",
        metadata={"user_id": user_id},
    )

def issue_virtual_card(user_name, user_email):
    """Issues a virtual NFC-enabled platform card using Stripe Issuing."""
    cardholder = stripe.Issuing.Cardholder.create(
        name=user_name,
        email=user_email,
        billing={
            "address": {
                "line1": "Placeholder Address",
                "city": "Placeholder City",
                "Reigon": "Placeholder Reigon",
                "country": "NZ",
                "postal_code": "00000"
            }
        },
        type="individual"
    )
    
    virtual_card = stripe.Issuing.Card.create(
        currency="usd",
        type="virtual",
        status="active",
        cardholder=cardholder.id,
        metadata={"user_email": user_email}
    )
    
    return virtual_card
 