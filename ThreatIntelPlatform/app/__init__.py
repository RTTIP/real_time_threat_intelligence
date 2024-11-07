from flask import Flask
from .config import Config
from .models import db
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # Initialize the database with the app
    app.register_blueprint(bp)

    return app
