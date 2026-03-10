# 🧑‍💻 Portfolio Development Documentation

## Project Overview

**Madhesh Cyberpunk Developer Portfolio**  
**Owner:** Madhesh Rasu A S

### Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML + Tailwind CSS
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **3D Animation:** Three.js
- **Image Processing:** Pillow
- **Deployment:** Render / Heroku

---

# 1️⃣ System Architecture

This portfolio system consists of **two main components**:

## 1.1 Public Website

Accessible to all visitors without authentication.

**Features:**
- Hero section with animated typing effect
- Three.js particle background
- Animated project showcase with hover effects
- Skills section with proficiency levels
- Blog posts with markdown support
- Contact form with validation
- Responsive mobile-friendly design
- Cyberpunk neon theme

## 1.2 Admin Dashboard

Protected by login authentication - only accessible by the owner.

**Admin Functions:**
- Add/edit/delete projects with image uploads
- Manage project showcase (featured/unfeatured)
- Create and publish blog posts
- Manage skills and proficiency levels
- Update portfolio settings (bio, tagline, theme color)
- Upload/manage resume PDF
- Upload profile picture
- Change theme color

### Architecture Pattern

```
User Browser
    ↓
Flask Web Server
    ↓
Routes (Public/Admin/Auth)
    ↓
Database Models
    ↓
SQLite/PostgreSQL Database
    ↓
Responses rendered by Jinja2 Templates
    ↓
HTML/CSS/JavaScript sent to browser
```

---

# 2️⃣ Project Folder Structure

```
madhesh-portfolio/
│
├── app.py                          # Flask app initialization
├── config.py                       # Configuration settings
├── run.py                          # Entry point
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (git-ignored)
├── .gitignore                      # Git ignore rules
│
├── models/                         # Database models
│   ├── __init__.py                # DB initialization & exports
│   ├── user.py                    # User model for admin auth
│   ├── project.py                 # Project model
│   ├── blog.py                    # BlogPost model
│   ├── skill.py                   # Skill model
│   └── settings.py                # Site settings model
│
├── routes/                         # Flask blueprints
│   ├── __init__.py
│   ├── public.py                  # Public routes (/, /projects, /blog, etc)
│   ├── admin.py                   # Admin routes (/admin/dashboard, etc)
│   └── auth.py                    # Authentication routes (/auth/login, etc)
│
├── forms/                          # WTForms for validation
│   ├── __init__.py
│   ├── auth_forms.py              # Login form
│   ├── project_forms.py           # Project creation/edit form
│   ├── blog_forms.py              # Blog post form
│   ├── skill_forms.py             # Skill form
│   ├── settings_forms.py          # Settings form
│   └── contact_form.py            # Contact form
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── helpers.py                 # File upload, image optimization, slug creation
│   └── decorators.py              # Custom decorators (admin_required)
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css              # Main stylesheet with cyberpunk theme
│   ├── js/
│   │   ├── three-background.js    # Three.js particle animation
│   │   ├── ai-animation.js        # AI-themed animations
│   │   ├── neural-network.js      # Neural network visualization
│   │   ├── matrix-rain.js         # Matrix rain effect
│   │   ├── scroll-animations.js   # Scroll-triggered animations
│   │   └── project-cards.js       # Project card interactions
│   └── uploads/                   # User uploaded files
│
├── templates/                      # Jinja2 templates
│   ├── base.html                  # Base template (extends to all pages)
│   ├── index.html                 # Home page
│   ├── about.html                 # About page
│   ├── projects.html              # Projects listing
│   ├── project_detail.html        # Single project detail
│   ├── blog.html                  # Blog listing
│   ├── blog_post.html             # Single blog post
│   ├── contact.html               # Contact form page
│   ├── 404.html                   # 404 error page
│   │
│   └── admin/                     # Admin templates
│       ├── base_admin.html        # Admin base template
│       ├── dashboard.html         # Admin dashboard
│       ├── login.html             # Admin login
│       ├── projects.html          # Admin: manage projects
│       ├── project_form.html      # Admin: add/edit project
│       ├── blogs.html             # Admin: manage blog posts
│       ├── blog_form.html         # Admin: add/edit blog
│       ├── skills.html            # Admin: manage skills
│       ├── skill_form.html        # Admin: add/edit skill
│       └── settings.html          # Admin: site settings
│
├── instance/                       # Instance folder (Flask)
│   └── portfolio.db                # SQLite database (auto-created)
│
└── .venv/                          # Virtual environment (git-ignored)
```

---

# 3️⃣ Database Design

### Database: SQLite (Development)

> **Note:** For production, PostgreSQL is recommended.

## 3.1 Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| username | String(64) | Unique username for admin login |
| password_hash | String(128) | Hashed password (using Werkzeug) |
| is_admin | Boolean | Admin privileges (default: True) |
| created_at | DateTime | Account creation timestamp |

**Model:** `models/user.py`

**Usage:** Admin authentication & user session management

```python
user = User(username='madhesh', is_admin=True)
user.set_password('password123')
db.session.add(user)
db.session.commit()
```

---

## 3.2 Projects Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| title | String(100) | Project title |
| description | Text | Short description |
| long_description | Text | Detailed description |
| image | String(200) | Path to project image |
| tech_stack | String(500) | Comma-separated technologies |
| github_link | String(200) | GitHub repository URL |
| demo_link | String(200) | Live demo URL |
| featured | Boolean | Show on homepage (default: False) |
| completed_date | Date | Project completion date |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

**Model:** `models/project.py`

**Helper Methods:**
- `get_tech_list()` - Returns tech_stack as a list

---

## 3.3 BlogPost Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| title | String(200) | Blog post title |
| slug | String(200) | URL-friendly slug (unique) |
| excerpt | String(300) | Short preview text |
| content | Text | Full blog content (supports markdown) |
| image | String(200) | Featured image path |
| published | Boolean | Is article published (default: False) |
| views | Integer | View count for analytics |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

**Model:** `models/blog.py`

---

## 3.4 Skills Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String(50) | Skill name (e.g., "Python", "React") |
| category | String(50) | Category (e.g., "programming", "framework", "tool") |
| level | Integer | Proficiency level (0-100) |
| icon | String(50) | Font Awesome icon class (e.g., "fab fa-python") |
| display_order | Integer | Display order (lower first) |

**Model:** `models/skill.py`

---

## 3.5 Settings Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| bio | Text | Biography/About text |
| tagline | String(200) | Professional tagline |
| profile_image | String(200) | Profile picture path |
| theme_color | String(7) | Hex color code (e.g., "#00ff00") |
| resume_path | String(200) | Path to resume PDF |
| github_url | String(200) | GitHub profile URL |
| linkedin_url | String(200) | LinkedIn profile URL |
| twitter_url | String(200) | Twitter profile URL |
| email | String(100) | Contact email |
| updated_at | DateTime | Last update timestamp |

**Model:** `models/settings.py`

---

# 4️⃣ Backend Development

## 4.1 Flask Application Setup

**File:** `app.py`

**Initialization Process:**
1. Create Flask app instance
2. Load configuration from `config.py`
3. Initialize extensions (db, login_manager, csrf)
4. Create upload directories
5. Register blueprints (routes)
6. Create database tables on first run
7. Create default admin user if doesn't exist
8. Create default settings if doesn't exist

**Example:**
```python
from app import create_app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

---

## 4.2 Routing System

### 4.2.1 Public Routes (`routes/public.py`)

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page with featured projects |
| `/about` | GET | About page with skills |
| `/projects` | GET | Paginated projects list |
| `/project/<id>` | GET | Single project detail |
| `/blog` | GET | Paginated blog posts |
| `/blog/<slug>` | GET | Single blog post |
| `/contact` | GET/POST | Contact form |

**Example Route:**
```python
@public_bp.route('/projects')
def projects():
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.created_at.desc())\
        .paginate(page=page, per_page=6, error_out=False)
    return render_template('projects.html', projects=projects)
```

---

### 4.2.2 Authentication Routes (`routes/auth.py`)

| Route | Method | Purpose |
|-------|--------|---------|
| `/auth/login` | GET/POST | Admin login page |
| `/auth/logout` | GET | Logout and redirect to home |

**Login Flow:**
1. User submits username and password
2. Query User table for matching username
3. Verify password hash using `check_password()`
4. Create session with Flask-Login
5. Redirect to admin dashboard or next page

---

### 4.2.3 Admin Routes (`routes/admin.py`)

| Route | Method | Purpose |
|-------|--------|---------|
| `/admin/` | GET | Dashboard with statistics |
| `/admin/projects` | GET | List all projects |
| `/admin/project/new` | GET/POST | Create new project |
| `/admin/project/<id>/edit` | GET/POST | Edit project |
| `/admin/project/<id>/delete` | POST | Delete project |
| `/admin/blogs` | GET | List all blog posts |
| `/admin/blog/new` | GET/POST | Create new blog post |
| `/admin/blog/<id>/edit` | GET/POST | Edit blog post |
| `/admin/blog/<id>/delete` | POST | Delete blog post |
| `/admin/skills` | GET | List all skills |
| `/admin/skill/new` | GET/POST | Create new skill |
| `/admin/skill/<id>/edit` | GET/POST | Edit skill |
| `/admin/skill/<id>/delete` | POST | Delete skill |
| `/admin/settings` | GET/POST | Edit site settings |

**Protection:** All admin routes require `@login_required` decorator

---

# 5️⃣ Frontend Development

## 5.1 Template Engine

Flask uses **Jinja2** template engine for rendering HTML with dynamic content.

**Base Template:** `templates/base.html`

All pages extend the base template:
```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <!-- Page content here -->
{% endblock %}
```

---

## 5.2 CSS Framework

**Framework:** Tailwind CSS + Custom CSS

### Tailwind CSS Setup

For production, add to `base.html`:
```html
<script src="https://cdn.tailwindcss.com"></script>
```

### Custom Stylesheets

1. **style.css** - Main styles (layout, typography, components)
2. **cyberpunk.css** - Neon theme with glow effects

---

## 5.3 Cyberpunk Theme

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Neon Blue | #00d4ff | Primary color, borders, text |
| Neon Pink | #ff006e | Accent color, highlights |
| Neon Purple | #b537f2 | Secondary accent |
| Neon Green | #39ff14 | Success, highlights |
| Dark BG | #0a0e27 | Main background |
| Card BG | #1a1f3a | Card/section background |

### CSS Classes

```css
.neon-text        /* Text with cyan glow */
.neon-border      /* Border with glow effect */
.cyber-card       /* Card with cyberpunk styling */
.scanlines        /* Retro scanlines effect */
.grid-bg          /* Animated grid background */
.glitch           /* Glitch text effect */
```

---

# 6️⃣ Animations

## 6.1 Three.js Particle Background

**File:** `static/js/three-background.js`

**Features:**
- 500 animated floating particles
- Cyan neon color (#00d4ff)
- Responsive to viewport size
- Smooth animation loop

**Implementation:**
```html
<div id="three-background"></div>
<script src="{{ url_for('static', filename='js/three-background.js') }}"></script>
```

> **Note:** Requires Three.js library included in HTML

---

## 6.2 Typing Effect

**File:** `static/js/typing-effect.js`

**Features:**
- Cycles through multiple text strings
- Typing and deleting animation
- Configurable speed and delays

**Usage:**
```html
<div class="typing-effect" id="typing-text"></div>

<script>
new TypingEffect('typing-text', [
    'Cybersecurity Student',
    'AI Builder',
    'Creative Technologist'
], 100, 2000);
</script>
```

---

## 6.3 Scroll Animations

**File:** `static/js/scroll-animations.js`

**Features:**
- Triggers animations when elements enter viewport
- Fade in, slide up, scale animations
- Uses Intersection Observer API

**Setup:**
```html
<div class="fade-in">Fades in on scroll</div>
<div data-animate="slide-in">Slides in on scroll</div>
```

---

## 6.4 Project Card Interactions

**File:** `static/js/project-cards.js`

**Features:**
- Hover effects (border glow, overlay)
- Tilt animation
- Click to open project details
- Smooth transitions

---

# 7️⃣ File Upload System

## 7.1 Upload Configuration

**Settings in `config.py`:**
```python
UPLOAD_FOLDER = 'static/uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'svg'}
```

## 7.2 Upload Structure

```
static/uploads/
├── projects/        # Project images (png, jpg, jpeg, gif)
├── blog/           # Blog featured images
├── resume/         # Resume PDFs
└── profile/        # Profile picture
```

## 7.3 Helper Functions (`utils/helpers.py`)

### `save_file(file, subfolder='')`

Saves uploaded file with validation.

**Parameters:**
- `file`: File object from form
- `subfolder`: Subdirectory under uploads (e.g., 'projects')

**Returns:** Filename (str) or None

**Features:**
- Validates file extension
- Generates unique filename with UUID
- Creates subdirectory if missing
- Optimizes images (resize, compress)

**Example:**
```python
from utils.helpers import save_file

filename = save_file(
    request.files['image'],
    subfolder='projects'
)
# Returns: '550e8400e29b41d4a716446655440000.jpg'
```

### `delete_file(filename, subfolder='')`

Deletes uploaded file.

**Example:**
```python
from utils.helpers import delete_file

delete_file('550e8400e29b41d4a716446655440000.jpg', 'projects')
```

### `optimize_image(file_path, max_size=(1200, 1200), quality=85)`

Optimizes image size and quality using Pillow.

**Features:**
- Resizes to max dimensions
- Compresses to specified quality
- Uses LANCZOS resampling

---

# 8️⃣ Contact Form System

## 8.1 Contact Form (`forms/contact_form.py`)

```python
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    subject = StringField('Subject', validators=[
        DataRequired(),
        Length(min=5, max=200)
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, max=2000)
    ])
    submit = SubmitField('Send Message')
```

## 8.2 Routes

**Form Submission:**
```python
@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # TODO: Store in database or send email
        flash('Message sent successfully!', 'success')
        return redirect(url_for('public.index'))
    return render_template('contact.html', form=form)
```

---

# 9️⃣ Security Implementation

## 9.1 Authentication

- **Password Hashing:** Werkzeug `generate_password_hash()` with PBKDF2
- **Session Management:** Flask-Login extension
- **Login Required:** `@login_required` decorator on protected routes

## 9.2 CSRF Protection

- **Form Protection:** `@csrf.exempt` option available for API routes
- **Form Token:** Automatically included in all forms

```html
{{ form.csrf_token }}
```

## 9.3 Authorization

- **Admin Required:** Custom `@admin_required` decorator
- **Owner Check:** Verify user owns resource before edit/delete

## 9.4 Input Validation

- **WTForms Validation:** Client & server-side validation
- **File Validation:** Check file extension and size
- **SQL Injection Prevention:** Using SQLAlchemy ORM (parameterized queries)

---

# 🔟 Configuration Management

## 10.1 Config File (`config.py`)

```python
class Config:
    # Basic Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///portfolio.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'svg'}
    
    # Admin Credentials
    ADMIN_USERNAME = 'madhesh'
    ADMIN_PASSWORD = 'cyberpunk123'  # Change this!
```

## 10.2 Environment Variables (`.env`)

```env
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here-change-in-prod
DATABASE_URL=sqlite:///portfolio.db
```

---

# 1️⃣1️⃣ Deployment

## 11.1 Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Change `SECRET_KEY` to strong random value
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Add security headers
- [ ] Minify CSS and JavaScript
- [ ] Optimize images
- [ ] Set up logging
- [ ] Configure CORS if needed
- [ ] Add robots.txt and sitemap.xml

## 11.2 Deploy to Render

**Steps:**

1. Push code to GitHub
2. Create account on Render.com
3. Create new Web Service
4. Connect GitHub repository
5. Set environment variables:
   ```
   FLASK_ENV=production
   PYTHON_VERSION=3.11
   ```
6. Deploy

**Procfile:**
```
web: gunicorn app:app
```

## 11.3 Deploy to Heroku

**Steps:**

1. Install Heroku CLI
2. Create Procfile with: `web: gunicorn app:app`
3. Create requirements.txt (already done)
4. `heroku create`
5. `git push heroku main`
6. `heroku key:set FLASK_ENV=production`

---

# 1️⃣2️⃣ Database Migrations

## 12.1 Manual Migration (Current Setup)

The application uses `db.create_all()` which creates all tables on first run. This is suitable for development.

## 12.2 Flask-Migrate for Production

For production, use Flask-Migrate:

```bash
pip install Flask-Migrate

# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Add new column"

# Apply migration
flask db upgrade
```

---

# 1️⃣3️⃣ Testing

## 13.1 Manual Testing Checklist

### Home Page
- [ ] Typing effect works
- [ ] Particle background visible
- [ ] Featured projects display correctly
- [ ] Navigation links work
- [ ] Responsive on mobile

### Projects Page
- [ ] Projects list loads
- [ ] Pagination works
- [ ] Project cards display properly
- [ ] Click opens project detail

### Project Detail
- [ ] Correct project information shown
- [ ] Image displays
- [ ] Tech stack shows
- [ ] Links (GitHub, Demo) work

### Blog
- [ ] Blog posts list loads
- [ ] Pagination works
- [ ] Click opens blog post

### Blog Post
- [ ] Content displays correctly
- [ ] Creation date shown
- [ ] Related posts shown (if implemented)

### Contact
- [ ] Form validates
- [ ] Required fields enforced
- [ ] Email validation works
- [ ] Message sends (check backend)

### Admin Login
- [ ] Login form appears
- [ ] Valid credentials login successfully
- [ ] Invalid credentials show error
- [ ] Redirect to dashboard on login

### Admin Dashboard
- [ ] Statistics display correctly
- [ ] Recent projects listed
- [ ] Recent blogs listed

### Admin Projects
- [ ] Add project form works
- [ ] Image upload works
- [ ] Edit project works
- [ ] Delete project works

### Admin Blog
- [ ] Add blog form works
- [ ] Edit works
- [ ] Delete works
- [ ] Publish/unpublish works

### Admin Settings
- [ ] Update bio
- [ ] Update tagline
- [ ] Change theme color
- [ ] Upload resume
- [ ] Upload profile image
- [ ] Update social links

---

# 1️⃣4️⃣ Performance Optimization

## 14.1 Image Optimization

- **Compression:** Pillow automatically compresses on upload
- **Resizing:** Images resized to max 1200x1200px
- **Format:** Convert to optimized formats (JPEG quality: 85)

## 14.2 Caching

Add to `config.py` for production:
```python
SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year for static files
```

## 14.3 Database Optimization

- **Indexing:** Add database indexes on frequently queried columns
- **Pagination:** Use pagination to limit database queries
- **Lazy Loading:** Use `lazy='select'` to avoid N+1 problem

## 14.4 Frontend Optimization

- **Minify CSS/JS:** Use tools like UglifyJS, cssnano
- **Lazy Load Images:** Use `loading="lazy"` attribute
- **CDN:** Serve static files from CDN (Cloudflare, AWS CloudFront)

---

# 1️⃣5️⃣ Development Workflow

## 15.1 Setup Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with dev settings
echo "FLASK_ENV=development" > .env
echo "SECRET_KEY=dev-key-change-in-production" >> .env

# Run Flask development server
python run.py
```

Access at http://localhost:5000

## 15.2 Making Changes

1. Edit files in `models/`, `routes/`, `templates/`, `static/`
2. Refresh browser (Flask auto-reloads on save)
3. Check terminal for errors
4. Test functionality

## 15.3 Adding New Routes

1. Create route function in appropriate file (`public.py` / `admin.py`)
2. Create @route decorator
3. Add @login_required/@admin_required if protected
4. Create template in `templates/`
5. Test in browser

**Example:**
```python
@public_bp.route('/new-page')
def new_page():
    return render_template('new_page.html')
```

---

# 1️⃣6️⃣ Common Issues & Solutions

## Issue: "ModuleNotFoundError: No module named '_____'"

**Solution:** Install missing package
```bash
pip install package-name
pip freeze > requirements.txt  # Update requirements
```

## Issue: "TemplateNotFound: filename.html"

**Solution:** Check template filename and path in `templates/` directory

## Issue: Database errors

**Solution:** Delete `portfolio.db` and restart app (recreates database)

## Issue: Static files not loading

**Solution:** Check URL_FOR usage and ensure files exist in `static/`

---

# 1️⃣7️⃣ Additional Features

## 17.1 Email Notifications (TODO)

Install Flask-Mail:
```bash
pip install Flask-Mail
```

Configure in `config.py` and send email on contact form submission.

## 17.2 Analytics (TODO)

Track:
- Page views
- Blog post views
- Project clicks
- Contact form submissions

## 17.3 Dark/Light Mode Toggle (TODO)

Store user preference in browser localStorage and toggle theme dynamically.

## 17.4 Search Functionality (TODO)

Implement search across projects and blog posts.

## 17.5 Comments on Blog Posts (TODO)

Add comments table and comment system for blog posts.

---

# 1️⃣8️⃣ Dependencies

All required packages are listed in `requirements.txt`:

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-WTF==1.1.1
python-dotenv==1.0.0
WTForms==3.0.1
email-validator==2.0.0
Werkzeug==2.3.7
Jinja2==3.1.2
Pillow==10.0.0
```

Install all: `pip install -r requirements.txt`

---

# 1️⃣9️⃣ Directory Structure (Complete)

```
madhesh-portfolio/
├── app.py                          # Flask app factory
├── config.py                       # Configuration
├── run.py                          # Entry point
├── requirements.txt                # Dependencies
├── .env                            # Environment variables
├── .gitignore                      # Git ignore
├── DOCUMENTATION.md                # This file
├── portfolio.db                    # SQLite database (auto-created)
│
├── models/
│   ├── __init__.py                 # db initialization
│   ├── user.py                     # User model
│   ├── project.py                  # Project model
│   ├── blog.py                     # BlogPost model
│   ├── skill.py                    # Skill model
│   └── settings.py                 # Settings model
│
├── routes/
│   ├── __init__.py
│   ├── public.py                   # Public page routes
│   ├── admin.py                    # Admin management routes
│   └── auth.py                     # Login/logout routes
│
├── forms/
│   ├── __init__.py
│   ├── auth_forms.py               # LoginForm
│   ├── project_forms.py            # ProjectForm
│   ├── blog_forms.py               # BlogPostForm
│   ├── skill_forms.py              # SkillForm
│   ├── settings_forms.py           # SettingsForm
│   └── contact_form.py             # ContactForm
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py                  # File upload, image optimization
│   └── decorators.py               # Custom decorators
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── cyberpunk.css
│   ├── js/
│   │   ├── three-background.js
│   │   ├── typing-effect.js
│   │   ├── scroll-animations.js
│   │   └── project-cards.js
│   └── uploads/
│       ├── projects/
│       ├── blog/
│       ├── resume/
│       └── profile/
│
└── templates/
    ├── base.html
    ├── index.html
    ├── about.html
    ├── projects.html
    ├── project_detail.html
    ├── blog.html
    ├── blog_post.html
    ├── contact.html
    ├── 404.html
    │
    └── admin/
        ├── base_admin.html
        ├── dashboard.html
        ├── login.html
        ├── projects.html
        ├── project_form.html
        ├── blogs.html
        ├── blog_form.html
        ├── skills.html
        ├── skill_form.html
        └── settings.html
```

---

# 2️⃣0️⃣ Quick Reference

## Routes

**Homepage:**
```
http://localhost:5000/
```

**Admin:**
```
http://localhost:5000/auth/login
http://localhost:5000/admin/
```

## Default Admin Credentials

Username: `madhesh`  
Password: `cyberpunk123`  

⚠️ **Change these immediately in production!**

## File Paths

- **Database:** `portfolio.db` (root)
- **Uploads:** `static/uploads/`
- **Templates:** `templates/`
- **Static files:** `static/css/`, `static/js/`

---

# 2️⃣1️⃣ Support & Improvements

## If You Encounter Issues:

1. Check error messages in terminal
2. Verify file paths are correct
3. Ensure all dependencies installed: `pip install -r requirements.txt`
4. Check `.env` file exists
5. Look in browser console (F12) for frontend errors

## Future Enhancements:

- [ ] Email notifications
- [ ] Blog comments system
- [ ] Dark mode toggle
- [ ] SEO improvements
- [ ] Analytics dashboard
- [ ] CDN integration
- [ ] Automated backups
- [ ] Rate limiting
- [ ] Admin user management
- [ ] Two-factor authentication

---

**Last Updated:** March 9, 2026  
**Version:** 1.0.0  
**Developer:** GitHub Copilot

---

**Happy coding! 🚀**
