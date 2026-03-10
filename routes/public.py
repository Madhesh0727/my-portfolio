from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_file
from models import Project, BlogPost, Skill, Settings, Message
from forms.contact_form import ContactForm
from app import db
import os
from io import BytesIO
from PIL import Image, ImageDraw

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    settings = Settings.query.first()
    featured_projects = Project.query.filter_by(featured=True).order_by(Project.created_at.desc()).limit(4).all()
    recent_posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    skills = Skill.query.order_by(Skill.display_order).all()
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    return render_template('index.html',
                         settings=settings,
                         featured_projects=featured_projects,
                         recent_posts=recent_posts,
                         skills_by_category=skills_by_category)

@public_bp.route('/about')
def about():
    settings = Settings.query.first()
    skills = Skill.query.order_by(Skill.display_order).all()
    
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    return render_template('about.html', settings=settings, skills_by_category=skills_by_category)

@public_bp.route('/projects')
def projects():
    category = request.args.get('category', 'all')
    if category and category != 'all':
        projects = Project.query.filter_by(category=category).order_by(Project.created_at.desc()).all()
    else:
        projects = Project.query.order_by(Project.created_at.desc()).all()
    
    categories = db.session.query(Project.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('projects.html', projects=projects, categories=categories, current_category=category)

@public_bp.route('/project/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    return render_template('project_detail.html', project=project)

@public_bp.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    
    query = BlogPost.query.filter_by(published=True)
    if category and category != 'all':
        query = query.filter_by(category=category)
    
    posts = query.order_by(BlogPost.created_at.desc()).paginate(page=page, per_page=6, error_out=False)
    
    categories = db.session.query(BlogPost.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('blog.html', posts=posts, categories=categories, current_category=category)

@public_bp.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    post.views += 1
    db.session.commit()
    return render_template('blog_post.html', post=post)

@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    settings = Settings.query.first()
    
    if form.validate_on_submit():
        try:
            new_msg = Message(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            db.session.add(new_msg)
            db.session.commit()
            flash('TRANSMISSION SUCCESSFUL. I will respond to your node shortly.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('TRANSMISSION FAILED. Please check your data connection.', 'error')
            
        return redirect(url_for('public.contact'))
    
    return render_template('contact.html', form=form, settings=settings)

@public_bp.route('/download-resume')
def download_resume():
    settings = Settings.query.first()
    if settings and settings.resume_path:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'resume', settings.resume_path)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
    flash('Resume not found', 'error')
    return redirect(url_for('public.index'))

@public_bp.route('/circle-favicon.png')
def circle_favicon():
    settings = Settings.query.first()
    if settings and settings.profile_image:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile', settings.profile_image)
        if os.path.exists(file_path):
            try:
                img = Image.open(file_path).convert("RGBA")
                
                # Make it square
                min_dim = min(img.size)
                left = (img.width - min_dim) / 2
                top = (img.height - min_dim) / 2
                right = (img.width + min_dim) / 2
                bottom = (img.height + min_dim) / 2
                img = img.crop((left, top, right, bottom))
                img = img.resize((128, 128), Image.Resampling.LANCZOS)
                
                # Create circle mask
                mask = Image.new("L", img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)
                
                # Apply mask
                output = Image.new("RGBA", img.size, (0, 0, 0, 0))
                output.paste(img, (0, 0), mask=mask)
                
                # Save to bytes
                img_io = BytesIO()
                output.save(img_io, 'PNG')
                img_io.seek(0)
                
                return send_file(img_io, mimetype='image/png')
            except Exception as e:
                pass
                
    fallback_path = os.path.join(current_app.root_path, 'static', 'favicon.ico')
    if os.path.exists(fallback_path):
        return send_file(fallback_path)
    return "", 404

@public_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@public_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500