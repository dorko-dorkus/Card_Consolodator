from cryptography.fernet import Fernet
import os
import stripe
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.config import Config

# Initialize Flask extensions
# SQLAlchemy for database management
db = SQLAlchemy()
# Bcrypt for password hashing
bcrypt = Bcrypt()
# LoginManager for handling user authentication
login_manager = LoginManager()

# Load Stripe secret key from environment variables
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if not STRIPE_SECRET_KEY:
    raise ValueError("Stripe Secret Key not set in environment variables")
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

    # Register application blueprints (routes)
    #from app.routes import consolidation_bp
    #app.register_blueprint(consolidation_bp, url_prefix='/api')

    return app
