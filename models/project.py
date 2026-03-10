from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    long_description = db.Column(db.Text)
    image = db.Column(db.Text)  # Comma-separated or single string
    tech_stack = db.Column(db.String(500))  # Comma-separated
    github_link = db.Column(db.String(200))
    demo_link = db.Column(db.String(200))
    featured = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50), default='AI/ML')
    completed_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_tech_list(self):
        if self.tech_stack:
            return [tech.strip() for tech in self.tech_stack.split(',')]
        return []
        
    def get_images_list(self):
        if self.image:
            return [img.strip() for img in self.image.split(',')]
        return []
        
    def get_primary_image(self):
        images = self.get_images_list()
        if images:
            return images[0]
        return None
    
    def __repr__(self):
        return f'<Project {self.title}>'