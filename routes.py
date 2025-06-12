from cryptography.fernet import Fernet
import os
import stripe

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
    except stripe.error.StripeError as e:
        return False