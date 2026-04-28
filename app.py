from flask import Flask, has_request_context, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import inspect, text
from config import Config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def ensure_upload_folders(app):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    for folder in ('projects', 'blog', 'profile', 'resume'):
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], folder), exist_ok=True)


def sync_optional_columns():
    inspector = inspect(db.engine)
    columns_to_add = {
        'settings': {
            'resume_template': "VARCHAR(50) DEFAULT 'resume_default.html'",
            'location': "VARCHAR(200)",
            'specialty': "VARCHAR(200)",
        },
        'education': {
            'cgpa': "VARCHAR(50)",
        },
        'projects': {
            'tech_stack': "TEXT",
            'demo_link': "VARCHAR(200)",
            'github_link': "VARCHAR(200)",
        },
        'blog_posts': {
            'excerpt': "TEXT",
            'views': "INTEGER DEFAULT 0",
        },
    }

    existing_tables = set(inspector.get_table_names())
    with db.engine.begin() as connection:
        for table_name, columns in columns_to_add.items():
            if table_name not in existing_tables:
                continue

            existing_columns = {
                column['name'] for column in inspector.get_columns(table_name)
            }
            for column_name, column_type in columns.items():
                if column_name in existing_columns:
                    continue
                connection.execute(
                    text(
                        f"ALTER TABLE {table_name} "
                        f"ADD COLUMN {column_name} {column_type}"
                    )
                )

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    ensure_upload_folders(app)
    
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
        from utils.site_data import get_settings_cached, get_unread_message_count

        try:
            settings_obj = get_settings_cached()
            if settings_obj:
                settings_obj.message_count = (
                    get_unread_message_count()
                    if has_request_context() and request.path.startswith('/admin')
                    else 0
                )
            return dict(settings=settings_obj)
        except Exception:
            return dict(settings=None)
            
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            sync_optional_columns()
        except Exception as e:
            print(f"Database initialization error: {e}")
        
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
