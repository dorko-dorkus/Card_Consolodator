# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key_here"

    env = os.getenv("FLASK_ENV", "production")
    if env == "development":
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///site.db")
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
        if not SQLALCHEMY_DATABASE_URI:
            raise RuntimeError("DATABASE_URL must be set for non-development environments")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Stripe Configuration
    # Default Stripe API keys for development/testing. These can be overridden
    # by environment variables in production deployments.
    STRIPE_SECRET_KEY = os.environ.get(
        'STRIPE_SECRET_KEY',
        'your_stripe_secret_key_here'
    )
    STRIPE_PUBLISHABLE_KEY = os.environ.get(
        'STRIPE_PUBLISHABLE_KEY',
        'your_stripe_publishable_key_here'
    )
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'your_stripe_webhook_secret_here')

    # Comma-separated list of origins allowed to access the API
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
