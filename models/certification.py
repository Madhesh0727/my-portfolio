from app import db
from datetime import datetime

class Certification(db.Model):
    __tablename__ = 'certification'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200), nullable=False)
    date_earned = db.Column(db.String(50))
    url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Certification {self.name}>'
