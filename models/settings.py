from app import db
from datetime import datetime

class Settings(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default="MADHESH")
    owner_name = db.Column(db.String(100), default="MADHESH RASU A S")
    contact_text = db.Column(db.Text, default="I'm always interested in hearing about new opportunities in AI/ML and cybersecurity.")
    contact_page_text = db.Column(db.Text, default="Opening a secure channel. Have an opportunity or project? My neural network is always listening for new challenges in AI/ML and Security.")
    bio = db.Column(db.Text, default="")
    what_i_do = db.Column(db.Text, default="Build responsive and interactive web applications\nDevelop secure backend systems with Python & Flask\nDesign cybersecurity solutions and implementations\nWork with AI/ML technologies for innovative solutions")
    tagline = db.Column(db.String(200), default="AI/ML Engineer & Cybersecurity Researcher")
    profile_image = db.Column(db.String(200), nullable=True)
    theme_color = db.Column(db.String(7), default='#00ff00')
    resume_path = db.Column(db.String(200), nullable=True)
    
    # Social links
    github_url = db.Column(db.String(200), default='https://github.com/madhesh')
    linkedin_url = db.Column(db.String(200), default='https://linkedin.com/in/madhesh')
    twitter_url = db.Column(db.String(200), nullable=True)
    instagram_url = db.Column(db.String(200), nullable=True)
    whatsapp_url = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), default='madhesh@example.com')
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Settings {self.id}>'