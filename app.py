from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure upload folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'projects'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'blog'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profile'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'resume'), exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Login manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access the admin area.'
    login_manager.login_message_category = 'warning'
    
    # Register blueprints
    from routes.public import public_bp
    from routes.admin import admin_bp
    from routes.auth import auth_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    @app.context_processor
    def inject_settings():
        from models.settings import Settings
        from models.message import Message
        try:
            settings_obj = Settings.query.first()
            if settings_obj:
                settings_obj.message_count = Message.query.filter_by(is_read=False).count()
            return dict(settings=settings_obj)
        except:
            return dict(settings=None)
            
    # Create database tables
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Create default admin user if not exists
        from models.user import User
        from models.settings import Settings
        
        if not User.query.first():
            admin = User(
                username=app.config['ADMIN_USERNAME'],
                is_admin=True
            )
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created: {app.config['ADMIN_USERNAME']}")
        
        # Create default settings if not exists
        if not Settings.query.first():
            settings = Settings(
                bio="Cybersecurity Student & AI/ML Enthusiast building the future with neural networks and creative code.",
                what_i_do="Build responsive and interactive web applications\nDevelop secure backend systems with Python & Flask\nDesign cybersecurity solutions and implementations\nWork with AI/ML technologies for innovative solutions",
                tagline="AI/ML Engineer | Cybersecurity Researcher | Neural Network Architect",
                theme_color="#00ff00",
                github_url="https://github.com/madhesh",
                linkedin_url="https://linkedin.com/in/madhesh",
                email="madhesh0727@gmail.com",
                location="Chennai, India",
                specialty="AI/ML, Cybersecurity"
            )
            db.session.add(settings)
            db.session.commit()
            print("Default settings created")
    
    # Security Headers for production readiness
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        if app.config.get('SESSION_COOKIE_SECURE'):
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    return app