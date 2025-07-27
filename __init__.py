from cryptography.fernet import Fernet
import os
import stripe

try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_bcrypt import Bcrypt
    from flask_login import LoginManager
except ModuleNotFoundError:  # Flask not installed during lightweight use or tests
    Flask = None
    SQLAlchemy = None
    Bcrypt = None
    LoginManager = None

try:
    # When installed as a package `app`, config may live in app.config
    from app.config import Config
except Exception:
    # Fallback to local config module
    from config import Config

# Initialize Flask extensions only if Flask is available
if Flask:
    # SQLAlchemy for database management
    db = SQLAlchemy()
    # Bcrypt for password hashing
    bcrypt = Bcrypt()
    # LoginManager for handling user authentication
    login_manager = LoginManager()
else:
    db = None
    bcrypt = None
    login_manager = None

# Load Stripe secret key from environment variables
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")
# Set Stripe API key for payment processing (tests may use placeholder)
stripe.api_key = STRIPE_SECRET_KEY

def create_app():
    """
    Application factory function to initialize and configure the Flask app.
    """
    if not Flask:
        raise RuntimeError("Flask is required to create the application")

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the Flask app
    if db is not None:
        db.init_app(app)
    if bcrypt is not None:
        bcrypt.init_app(app)
    if login_manager is not None:
        login_manager.init_app(app)

    # Register application blueprints (routes)
    #from app.routes import consolidation_bp
    #app.register_blueprint(consolidation_bp, url_prefix='/api')

    return app
