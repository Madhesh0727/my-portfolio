import sqlite3
import os

def migrate():
    db_path = os.path.join('instance', 'portfolio.db')
    if not os.path.exists(db_path):
        # Maybe it's not created yet or in a different path
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE education ADD COLUMN cgpa VARCHAR(50)")
        print("Added cgpa to education")
    except sqlite3.OperationalError as e:
        print("Education cgpa might already exist:", e)

    try:
        cursor.execute("ALTER TABLE settings ADD COLUMN resume_template VARCHAR(50) DEFAULT 'resume_default.html'")
        print("Added resume_template to settings")
    except sqlite3.OperationalError as e:
        print("Settings resume_template might already exist:", e)
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
