from app import create_app, db
from sqlalchemy import text
import sys

def migrate():
    app = create_app()
    with app.app_context():
        # Check what columns exist in the settings table
        # We'll use a try-except block with raw SQL for maximum compatibility
        
        # 1. Add resume_template to settings if missing
        try:
            db.session.execute(text("ALTER TABLE settings ADD COLUMN resume_template VARCHAR(50) DEFAULT 'resume_default.html'"))
            db.session.commit()
            print("Successfully added resume_template to settings table.")
        except Exception as e:
            db.session.rollback()
            print(f"Skipping resume_template (it might already exist): {e}")

        # 2. Add cgpa to education if missing
        try:
            db.session.execute(text("ALTER TABLE education ADD COLUMN cgpa VARCHAR(50)"))
            db.session.commit()
            print("Successfully added cgpa to education table.")
        except Exception as e:
            db.session.rollback()
            print(f"Skipping cgpa (it might already exist): {e}")

        # 3. Add location to settings if missing (sometimes helpful to check all new fields)
        try:
            db.session.execute(text("ALTER TABLE settings ADD COLUMN location VARCHAR(200)"))
            db.session.commit()
            print("Successfully added location to settings table.")
        except Exception as e:
            db.session.rollback()
            print(f"Skipping location (it might already exist): {e}")

        # 4. Add specialty to settings if missing
        try:
            db.session.execute(text("ALTER TABLE settings ADD COLUMN specialty VARCHAR(200)"))
            db.session.commit()
            print("Successfully added specialty to settings table.")
        except Exception as e:
            db.session.rollback()
            print(f"Skipping specialty (it might already exist): {e}")

        # 5. Add tech_stack, demo_link, github_link to projects if missing
        for col in [('tech_stack', 'TEXT'), ('demo_link', 'VARCHAR(200)'), ('github_link', 'VARCHAR(200)')]:
            try:
                db.session.execute(text(f"ALTER TABLE projects ADD COLUMN {col[0]} {col[1]}"))
                db.session.commit()
                print(f"Successfully added {col[0]} to projects table.")
            except Exception as e:
                db.session.rollback()
                print(f"Skipping {col[0]} in projects: {e}")

        # 6. Add excerpt, views to blog_posts if missing
        for col in [('excerpt', 'TEXT'), ('views', 'INTEGER DEFAULT 0')]:
            try:
                db.session.execute(text(f"ALTER TABLE blog_posts ADD COLUMN {col[0]} {col[1]}"))
                db.session.commit()
                print(f"Successfully added {col[0]} to blog_posts table.")
            except Exception as e:
                db.session.rollback()
                print(f"Skipping {col[0]} in blog_posts: {e}")

        print("Migration process complete.")

if __name__ == "__main__":
    migrate()
