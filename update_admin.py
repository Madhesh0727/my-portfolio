import os
from app import create_app, db
from models.user import User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(username='madhesh').first() # Get the old user
    if not admin:
        admin = User.query.first() # Getting any first user if 'madhesh' was changed

    if admin:
        # Update username and password to new config
        old_username = admin.username
        admin.username = app.config['ADMIN_USERNAME']
        admin.set_password(app.config['ADMIN_PASSWORD'])
        db.session.commit()
        print(f"✅ Successfully updated admin credentials in database!")
        print(f"Old Username: {old_username}")
        print(f"New Username: {admin.username}")
        print("Password has been changed to the one in config.py")
    else:
        print("❌ No admin user found in database.")
