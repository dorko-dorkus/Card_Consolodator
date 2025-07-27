from app import create_app, db
from flask_migrate import Migrate

app = create_app()

migrate = Migrate(app, db)

# Import models for Alembic's autogenerate feature
from app import models  # noqa: F401

if __name__ == '__main__':
    app.run()
