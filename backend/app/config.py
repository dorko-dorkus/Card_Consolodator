# app/config.py
import os

class Config:
    """Application configuration loaded from environment variables."""

    env = os.getenv("FLASK_ENV", "production")

    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key_here"
    if env != "development" and SECRET_KEY == "your_secret_key_here":
        raise RuntimeError("SECRET_KEY environment variable must be set for production")

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

    if env != "development" and (
        STRIPE_SECRET_KEY == 'your_stripe_secret_key_here'
        or STRIPE_PUBLISHABLE_KEY == 'your_stripe_publishable_key_here'
        or STRIPE_WEBHOOK_SECRET == 'your_stripe_webhook_secret_here'
    ):
        raise RuntimeError('Stripe keys must be configured for production')

    # Comma-separated list of origins allowed to access the API
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

    # Global rate limit for the API, used by Flask-Limiter
    RATE_LIMIT = os.environ.get('RATE_LIMIT', '100/hour')
    # Veriff configuration
    VERIFF_API_KEY = os.environ.get("VERIFF_API_KEY")
    VERIFF_BASE_URL = os.environ.get("VERIFF_BASE_URL", "https://api.veriff.me/v1")

