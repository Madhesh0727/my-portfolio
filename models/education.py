from app import db
from datetime import datetime

class Education(db.Model):
    __tablename__ = 'education'
    
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(200), nullable=False)
    college = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    cgpa = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Education {self.degree}>'
