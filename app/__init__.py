from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_wtf.csrf import CSRFProtect
from .config import Config  


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
   
    CSRFProtect(app)

    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models (required for Flask-Migrate)
    from .models import Movie

    # Register blueprints
    from .views import bp
    app.register_blueprint(bp)

    return app