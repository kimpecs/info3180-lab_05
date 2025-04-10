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
    
    # Initialize CSRF protection FIRST
    csrf = CSRFProtect(app)  # This line is sufficient
    
    # THEN create upload folder
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    # THEN initialize database
    db.init_app(app)
    migrate.init_app(app, db)
    
    # THEN import models and register blueprints
    with app.app_context():
        from .models import Movie
        db.create_all()
    
    from .views import bp
    app.register_blueprint(bp)
    
    return app