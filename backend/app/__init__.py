import os

from flask import Flask
from app.config import Config
from app.extensions import db, jwt, cors, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Khởi tạo extensions với app
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","))
    migrate.init_app(app, db)
    
    # Import và đăng ký blueprints
    from app.routes import auth_bp, customers_bp, messages_bp
    app.register_blueprint(auth_bp, url_prefix="/api/user")
    app.register_blueprint(customers_bp, url_prefix="/api/customers")
    app.register_blueprint(messages_bp, url_prefix="/api/messages")
    
    return app

    
    