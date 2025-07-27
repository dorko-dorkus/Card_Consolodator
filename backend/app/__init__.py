from cryptography.fernet import Fernet
import os
import stripe
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .config import Config

# Initialize Flask extensions
# SQLAlchemy for database management
db = SQLAlchemy()
# Bcrypt for password hashing
bcrypt = Bcrypt()
# LoginManager for handling user authentication
login_manager = LoginManager()

# Load Stripe secret key, falling back to the value defined in Config
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", Config.STRIPE_SECRET_KEY)
if not STRIPE_SECRET_KEY:
    raise ValueError("Stripe Secret Key not set in environment variables or configuration")
# Set Stripe API key for payment processing
stripe.api_key = STRIPE_SECRET_KEY

def create_app():
    """
    Application factory function to initialize and configure the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the Flask app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import models  # ensure models are registered for migrations

    # Register application blueprints (routes)
    from .routes import api_bp
    from .webhooks import webhooks_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(webhooks_bp, url_prefix='/api')

    return app
