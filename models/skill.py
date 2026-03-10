from app import db

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'ai-ml', 'cybersecurity', 'programming', 'tools'
    level = db.Column(db.Integer, default=80)  # 0-100
    icon = db.Column(db.String(50))
    display_order = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Skill {self.name}>'