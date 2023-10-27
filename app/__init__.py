from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    from .customers import customer_bp
    from .work_orders import orders_bp

    app.register_blueprint(customer_bp)
    app.register_blueprint(orders_bp)

    return app
