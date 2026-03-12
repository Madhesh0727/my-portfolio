from app import db
from datetime import datetime

class Experience(db.Model):
    __tablename__ = 'experience'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    description = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Experience {self.company}>'
