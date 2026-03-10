from app import db
from datetime import datetime

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    excerpt = db.Column(db.String(300))
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text)  # Comma-separated or single string
    category = db.Column(db.String(50), default='AI/ML')
    published = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
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
        return f'<BlogPost {self.title}>'