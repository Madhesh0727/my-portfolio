from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from models import Project, BlogPost, Skill, Settings, Message, Education, Experience, Certification
from forms.project_forms import ProjectForm
from forms.blog_forms import BlogPostForm
from forms.skill_forms import SkillForm
from forms.settings_forms import SettingsForm
from forms.education_forms import EducationForm
from forms.experience_forms import ExperienceForm
from forms.certification_forms import CertificationForm
from app import db
from utils.decorators import admin_required
from utils.helpers import save_file, delete_file, create_slug
from utils.site_data import clear_site_cache

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    project_count = Project.query.count()
    blog_count = BlogPost.query.count()
    skill_count = Skill.query.count()
    
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    recent_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         project_count=project_count,
                         blog_count=blog_count,
                         skill_count=skill_count,
                         recent_projects=recent_projects,
                         recent_posts=recent_posts)

# ========== PROJECT MANAGEMENT ==========
@admin_bp.route('/projects')
@login_required
@admin_required
def projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=projects)

@admin_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_project():
    form = ProjectForm()
    
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            long_description=form.long_description.data,
            tech_stack=form.tech_stack.data,
            github_link=form.github_link.data,
            demo_link=form.demo_link.data,
            featured=form.featured.data,
            category=form.category.data
        )
        
        images_list = []
        if form.image.data:
            for file in form.image.data:
                if hasattr(file, 'filename') and file.filename:
                    filename = save_file(file, 'projects')
                    if filename:
                        images_list.append(filename)
        if images_list:
            project.image = ','.join(images_list)
        
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html', form=form, title='New Project')

@admin_bp.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.long_description = form.long_description.data
        project.tech_stack = form.tech_stack.data
        project.github_link = form.github_link.data
        project.demo_link = form.demo_link.data
        project.featured = form.featured.data
        project.category = form.category.data
        
        # Replace images only if new files uploaded
        new_images = []
        if form.image.data:
            for file in form.image.data:
                if hasattr(file, 'filename') and file.filename:
                    filename = save_file(file, 'projects')
                    if filename:
                        new_images.append(filename)
                        
        if len(new_images) > 0:
            if project.image:
                delete_file(project.image, 'projects')
            project.image = ','.join(new_images)
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html', form=form, project=project, title='Edit Project')

@admin_bp.route('/projects/delete/<int:id>')
@login_required
@admin_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    if project.image:
        delete_file(project.image, 'projects')
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

# ========== BLOG MANAGEMENT ==========
@admin_bp.route('/blogs')
@login_required
@admin_required
def blogs():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blogs.html', posts=posts)

@admin_bp.route('/blogs/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_blog():
    form = BlogPostForm()
    
    if form.validate_on_submit():
        slug = create_slug(form.title.data)
        original_slug = slug
        counter = 1
        while BlogPost.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        post = BlogPost(
            title=form.title.data,
            slug=slug,
            excerpt=form.excerpt.data,
            content=form.content.data,
            published=form.published.data,
            category=form.category.data
        )
        
        images_list = []
        if form.image.data:
            for file in form.image.data:
                if hasattr(file, 'filename') and file.filename:
                    filename = save_file(file, 'blog')
                    if filename:
                        images_list.append(filename)
        if images_list:
            post.image = ','.join(images_list)
        
        db.session.add(post)
        db.session.commit()
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('admin.blogs'))
    
    return render_template('admin/blog_form.html', form=form, title='New Blog Post')

@admin_bp.route('/blogs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_blog(id):
    post = BlogPost.query.get_or_404(id)
    form = BlogPostForm(obj=post)
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.excerpt = form.excerpt.data
        post.content = form.content.data
        post.published = form.published.data
        post.category = form.category.data
        
        new_images = []
        if form.image.data:
            for file in form.image.data:
                if hasattr(file, 'filename') and file.filename:
                    filename = save_file(file, 'blog')
                    if filename:
                        new_images.append(filename)
        
        if len(new_images) > 0:
            if post.image:
                delete_file(post.image, 'blog')
            post.image = ','.join(new_images)
        
        db.session.commit()
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('admin.blogs'))
    
    return render_template('admin/blog_form.html', form=form, post=post, title='Edit Blog Post')

@admin_bp.route('/blogs/delete/<int:id>')
@login_required
@admin_required
def delete_blog(id):
    post = BlogPost.query.get_or_404(id)
    if post.image:
        delete_file(post.image, 'blog')
    db.session.delete(post)
    db.session.commit()
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('admin.blogs'))

# ========== SKILLS MANAGEMENT ==========
@admin_bp.route('/skills')
@login_required
@admin_required
def skills():
    skills = Skill.query.order_by(Skill.category, Skill.display_order).all()
    return render_template('admin/skills.html', skills=skills)

@admin_bp.route('/skills/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_skill():
    form = SkillForm()
    
    if form.validate_on_submit():
        skill = Skill(
            name=form.name.data,
            category=form.category.data,
            level=form.level.data,
            icon=form.icon.data,
            display_order=form.display_order.data
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('admin.skills'))
    
    return render_template('admin/skill_form.html', form=form, title='New Skill')

@admin_bp.route('/skills/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_skill(id):
    skill = Skill.query.get_or_404(id)
    form = SkillForm(obj=skill)
    
    if form.validate_on_submit():
        skill.name = form.name.data
        skill.category = form.category.data
        skill.level = form.level.data
        skill.icon = form.icon.data
        skill.display_order = form.display_order.data
        db.session.commit()
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('admin.skills'))
    
    return render_template('admin/skill_form.html', form=form, skill=skill, title='Edit Skill')

@admin_bp.route('/skills/delete/<int:id>')
@login_required
@admin_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin.skills'))

# ========== EDUCATION MANAGEMENT ==========
@admin_bp.route('/education')
@login_required
@admin_required
def education():
    education_list = Education.query.order_by(Education.display_order).all()
    return render_template('admin/education.html', education_list=education_list)

@admin_bp.route('/education/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_education():
    form = EducationForm()
    
    if form.validate_on_submit():
        education_item = Education(
            degree=form.degree.data,
            college=form.college.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            cgpa=form.cgpa.data,
            description=form.description.data,
            display_order=form.display_order.data
        )
        db.session.add(education_item)
        db.session.commit()
        flash('Education added successfully!', 'success')
        return redirect(url_for('admin.education'))
    
    return render_template('admin/education_form.html', form=form, title='New Education')

@admin_bp.route('/education/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_education(id):
    education_item = Education.query.get_or_404(id)
    form = EducationForm(obj=education_item)
    
    if form.validate_on_submit():
        education_item.degree = form.degree.data
        education_item.college = form.college.data
        education_item.start_date = form.start_date.data
        education_item.end_date = form.end_date.data
        education_item.cgpa = form.cgpa.data
        education_item.description = form.description.data
        education_item.display_order = form.display_order.data
        db.session.commit()
        flash('Education updated successfully!', 'success')
        return redirect(url_for('admin.education'))
    
    return render_template('admin/education_form.html', form=form, education=education_item, title='Edit Education')

@admin_bp.route('/education/delete/<int:id>')
@login_required
@admin_required
def delete_education(id):
    education_item = Education.query.get_or_404(id)
    db.session.delete(education_item)
    db.session.commit()
    flash('Education deleted successfully!', 'success')
    return redirect(url_for('admin.education'))

# ========== EXPERIENCE MANAGEMENT ==========
@admin_bp.route('/experience')
@login_required
@admin_required
def experience():
    experience_list = Experience.query.order_by(Experience.display_order).all()
    return render_template('admin/experience.html', experience_list=experience_list)

@admin_bp.route('/experience/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_experience():
    form = ExperienceForm()
    
    if form.validate_on_submit():
        exp_item = Experience(
            role=form.role.data,
            company=form.company.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            description=form.description.data,
            display_order=form.display_order.data
        )
        db.session.add(exp_item)
        db.session.commit()
        flash('Experience added successfully!', 'success')
        return redirect(url_for('admin.experience'))
    
    return render_template('admin/experience_form.html', form=form, title='New Experience')

@admin_bp.route('/experience/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_experience(id):
    exp_item = Experience.query.get_or_404(id)
    form = ExperienceForm(obj=exp_item)
    
    if form.validate_on_submit():
        exp_item.role = form.role.data
        exp_item.company = form.company.data
        exp_item.start_date = form.start_date.data
        exp_item.end_date = form.end_date.data
        exp_item.description = form.description.data
        exp_item.display_order = form.display_order.data
        db.session.commit()
        flash('Experience updated successfully!', 'success')
        return redirect(url_for('admin.experience'))
    
    return render_template('admin/experience_form.html', form=form, experience=exp_item, title='Edit Experience')

@admin_bp.route('/experience/delete/<int:id>')
@login_required
@admin_required
def delete_experience(id):
    exp_item = Experience.query.get_or_404(id)
    db.session.delete(exp_item)
    db.session.commit()
    flash('Experience deleted successfully!', 'success')
    return redirect(url_for('admin.experience'))

# ========== CERTIFICATION MANAGEMENT ==========
@admin_bp.route('/certifications')
@login_required
@admin_required
def certifications():
    cert_list = Certification.query.order_by(Certification.display_order).all()
    return render_template('admin/certifications.html', cert_list=cert_list)

@admin_bp.route('/certifications/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_certification():
    form = CertificationForm()
    
    if form.validate_on_submit():
        cert_item = Certification(
            name=form.name.data,
            issuer=form.issuer.data,
            date_earned=form.date_earned.data,
            url=form.url.data,
            description=form.description.data,
            display_order=form.display_order.data
        )
        db.session.add(cert_item)
        db.session.commit()
        flash('Certification added successfully!', 'success')
        return redirect(url_for('admin.certifications'))
    
    return render_template('admin/certification_form.html', form=form, title='New Certification')

@admin_bp.route('/certifications/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_certification(id):
    cert_item = Certification.query.get_or_404(id)
    form = CertificationForm(obj=cert_item)
    
    if form.validate_on_submit():
        cert_item.name = form.name.data
        cert_item.issuer = form.issuer.data
        cert_item.date_earned = form.date_earned.data
        cert_item.url = form.url.data
        cert_item.description = form.description.data
        cert_item.display_order = form.display_order.data
        db.session.commit()
        flash('Certification updated successfully!', 'success')
        return redirect(url_for('admin.certifications'))
    
    return render_template('admin/certification_form.html', form=form, certification=cert_item, title='Edit Certification')

@admin_bp.route('/certifications/delete/<int:id>')
@login_required
@admin_required
def delete_certification(id):
    cert_item = Certification.query.get_or_404(id)
    db.session.delete(cert_item)
    db.session.commit()
    flash('Certification deleted successfully!', 'success')
    return redirect(url_for('admin.certifications'))

# ========== SETTINGS MANAGEMENT ==========
@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        db.session.add(settings)
        db.session.commit()
    
    form = SettingsForm(obj=settings)
    if request.method == 'GET':
        form.admin_username.data = current_user.username
    
    if form.validate_on_submit():
        settings.site_name = form.site_name.data
        settings.owner_name = form.owner_name.data
        settings.contact_text = form.contact_text.data
        settings.contact_page_text = form.contact_page_text.data
        settings.bio = form.bio.data
        settings.what_i_do = form.what_i_do.data
        settings.tagline = form.tagline.data
        settings.theme_color = form.theme_color.data
        settings.github_url = form.github_url.data
        settings.linkedin_url = form.linkedin_url.data
        settings.twitter_url = form.twitter_url.data
        settings.instagram_url = form.instagram_url.data
        settings.whatsapp_url = form.whatsapp_url.data
        settings.email = form.email.data
        settings.location = form.location.data
        settings.specialty = form.specialty.data
        settings.resume_template = form.resume_template.data
        
        if form.profile_image.data and hasattr(form.profile_image.data, 'filename') and form.profile_image.data.filename:
            if settings.profile_image:
                delete_file(settings.profile_image, 'profile')
            filename = save_file(form.profile_image.data, 'profile')
            settings.profile_image = filename
        
        if form.resume.data and hasattr(form.resume.data, 'filename') and form.resume.data.filename:
            if settings.resume_path:
                delete_file(settings.resume_path, 'resume')
            filename = save_file(form.resume.data, 'resume')
            settings.resume_path = filename
        
        if form.admin_username.data and form.admin_username.data != current_user.username:
            current_user.username = form.admin_username.data
            try:
                import dotenv
                import os
                dotenv.set_key(os.path.join(current_app.root_path, '.env'), 'ADMIN_USERNAME', form.admin_username.data)
            except Exception:
                pass

        if form.new_password.data:
            current_user.set_password(form.new_password.data)
            try:
                import dotenv
                import os
                dotenv.set_key(os.path.join(current_app.root_path, '.env'), 'ADMIN_PASSWORD', form.new_password.data)
            except Exception:
                pass
        
        db.session.commit()
        clear_site_cache()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin.settings'))
    
    return render_template('admin/settings.html', form=form, settings=settings)

# ========== MESSAGES MANAGEMENT ==========
@admin_bp.route('/messages')
@login_required
@admin_required
def messages():
    all_messages = Message.query.order_by(Message.created_at.desc()).all()
    # Mark all retrieved messages as read
    for msg in all_messages:
        if not msg.is_read:
            msg.is_read = True
    db.session.commit()
    return render_template('admin/messages.html', messages=all_messages)

@admin_bp.route('/messages/delete/<int:id>')
@login_required
@admin_required
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash('Log erased from mainframe.', 'success')
    return redirect(url_for('admin.messages'))
