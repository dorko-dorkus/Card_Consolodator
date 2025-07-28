from cryptography.fernet import Fernet
import os
import stripe
import logging
import sys
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import Config

# Initialize Flask extensions
# SQLAlchemy for database management
db = SQLAlchemy()
# Bcrypt for password hashing
bcrypt = Bcrypt()
# LoginManager for handling user authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "api.login"
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback."""
    from .models import User
    return db.session.get(User, int(user_id))

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

    required_keys = {
        'SECRET_KEY': 'your_secret_key_here',
        'STRIPE_SECRET_KEY': 'your_stripe_secret_key_here',
        'STRIPE_PUBLISHABLE_KEY': 'your_stripe_publishable_key_here',
        'STRIPE_WEBHOOK_SECRET': 'your_stripe_webhook_secret_here',
    }

    for key, placeholder in required_keys.items():
        value = os.environ.get(key, app.config.get(key))
        if not value or value == placeholder:
            raise RuntimeError(f"{key} environment variable is required")

    # Configure logging to stdout or a file
    log_file = os.getenv("LOG_FILE")
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    handler = RotatingFileHandler(log_file, maxBytes=1048576, backupCount=1) if log_file else logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
    app.logger.setLevel(log_level)
    app.logger.handlers = [handler]

    # Configure CORS origins from environment or configuration
    allowed_origins = os.getenv("CORS_ORIGINS", Config.CORS_ORIGINS)
    origins_list = [o.strip() for o in allowed_origins.split(',')] if allowed_origins else "*"
    CORS(app, origins=origins_list, supports_credentials=True)

    # Disable CSRF in testing environments
    if 'pytest' in sys.modules:
        app.config['WTF_CSRF_ENABLED'] = False

    # Update rate limit from environment at runtime
    app.config['RATELIMIT_DEFAULT'] = os.getenv('RATE_LIMIT', app.config.get('RATELIMIT_DEFAULT', '100/hour'))

    # Initialize extensions with the Flask app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    app.config.setdefault('RATELIMIT_HEADERS_ENABLED', True)
    limiter.default_limits = [app.config['RATELIMIT_DEFAULT']]
    limiter.init_app(app)

    with app.app_context():
        from . import models  # ensure models are registered for migrations
        from .scheduled_tasks import init_scheduler
        init_scheduler(app)

    # Register application blueprints (routes)
    from .routes import api_bp
    from .webhooks import webhooks_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(webhooks_bp, url_prefix='/api')

    @app.after_request
    def set_csrf_cookie(response):
        if app.config.get('WTF_CSRF_ENABLED', True):
            from flask_wtf.csrf import generate_csrf
            response.set_cookie('csrf_token', generate_csrf())
        return response

    return app
