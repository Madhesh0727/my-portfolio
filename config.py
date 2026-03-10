import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Database
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'portfolio.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'svg', 'mp4', 'webm', 'ogg', 'mov'}
    
    # Session & Security
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Production security flags (set FLASK_ENV=production in .env to enable)
    is_prod = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_SECURE = is_prod
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = is_prod
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Admin credentials from env
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin@123')