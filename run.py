import os
from flask_migrate import Migrate
from app import create_app, db

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db)
