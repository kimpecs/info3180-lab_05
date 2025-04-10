import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent  
class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YourStrongSecretKeyHere!1234'
    
    # Upload Configuration - absolute path
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://lab5_user:DoveLove@localhost/lab5'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False