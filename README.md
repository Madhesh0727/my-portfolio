# 🧑‍💻 Madhesh Cyberpunk Developer Portfolio

A dynamic, animated cyberpunk-themed portfolio website built with **Flask**, **Tailwind CSS**, and **Three.js**. Fully equipped for production with specialized views, error handling, and robust data management.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Flask](https://img.shields.io/badge/flask-2.3.3-blue)

---

## 🌟 Features

### Public Website
- ✨ **Animated Hero Section** with typing effect
- 🎨 **Cyberpunk Neon Theme** with custom animations
- 📱 **Fully Responsive** design (mobile, tablet, desktop)
- 🖼️ **Image Optimization** featuring dynamic circular favicons and auto-scaling aspect-ratio (16:9) blog/project image carousels. 
- 📝 **Blog System** with post management
- 💼 **Skills Display** with proficiency levels
- 📧 **Contact Form** with validation
- 🎯 **SEO Optimized** structure
- ⛔ **Custom Cyberpunk Error Pages** dedicated 404 and 500 error displays matching the theme.

### Admin Dashboard
- 🔐 **Secure Login** with password hashing
- 📊 **Statistics Dashboard** (projects, blogs, skills count, transmission logs)
- ➕ **Add/Edit/Delete Projects** with image uploads (auto-deletes old images from server to save space)
- ✍️ **Create Blog Posts** with rich content (auto-deletes old media when updated)
- 🏆 **Manage Skills** and proficiency levels
- ⚙️ **Site Settings** (bio, tagline, theme color, resume upload)
- 👤 **Profile & Security Management** Update admin username, password (auto-syncs to `.env`), and profile picture directly from the panel.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone Repository**
   ```bash
   cd madhesh-portfolio
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` File**
   Create a `.env` file at the root of the project to securely house your credentials:
   ```env
   FLASK_ENV=development
   SECRET_KEY=your-super-secret-key-change-this-in-production-2024
   DATABASE_URL=sqlite:///portfolio.db
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=admin@123
   ```

5. **Run Development Server**
   ```bash
   python run.py
   ```

6. **Access Application**
   ```
   http://localhost:5000
   ```
   *To log into the Admin Panel, navigate to `/auth/login` holding the credentials you set in the `.env` file!*

---

## 📁 Project Structure

```
madhesh-portfolio/
├── app.py                    # Flask app initialization
├── config.py                 # Configuration settings
├── run.py                    # Development server entry point
├── wsgi.py                   # Production server entry point (Gunicorn)
├── update_admin.py           # Helper script to sync DB credentials
├── requirements.txt          # Python dependencies
├── DOCUMENTATION.md          # Detailed documentation
├── README.md                 # This file
│
├── models/                   # Database models
│   ├── user.py              # User authentication
│   ├── project.py           # Projects management
│   ├── blog.py              # Blog posts
│   ├── skill.py             # Skills/abilities
│   └── settings.py          # Site settings
│
├── routes/                   # Flask blueprints/routes
│   ├── public.py            # Public pages & dynamic views
│   ├── admin.py             # Admin dashboard operations
│   └── auth.py              # Authentication
│
├── forms/                    # WTForms validation
├── templates/               # HTML templates (incl. 404, 500)
├── static/                  # CSS, JS, images, uploads
└── portfolio.db             # SQLite database (auto-created)
```

---

## � Deployment (Production Ready)

The application has been outfitted with a standard `wsgi.py` entry point. It is strictly recommended to run the app using a production worker rather than the Flask native `run.py` server online.

### Deploy to Render / DigitalOcean App Platform

1. Connect your GitHub repository tracking this code.
2. In the setup, set the start command to:
   ```bash
   gunicorn wsgi:app
   ```
3. Set your internal Environment Variables (`SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`) within the provider's dashboard.
4. Deploy!

### Deploy to Heroku

```bash
pip install gunicorn
echo "web: gunicorn wsgi:app" > Procfile
git push heroku main
```

---

## 🔒 Security Features

- ✅ **Password Hashing** (Werkzeug)
- ✅ **Session Management** (Flask-Login)
- ✅ **CSRF Protection** (Flask-WTF)
- ✅ **Environment Variables Sync** (Dynamically overwrites `.env` when changed in UI)
- ✅ **Input Validation** (WTForms)
- ✅ **SQL Injection Prevention** (SQLAlchemy ORM)
- ✅ **Automated File Cleanup** (Wipes old medias on DB delete)

---

## 📦 Dependencies

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM database
- **Flask-Login** - User sessions
- **Flask-WTF** - Form validation
- **Pillow** - Image processing & dynamic avatar masking
- **python-dotenv** - Environment variables
- **Werkzeug** - Password hashing
- **Gunicorn** - Production WSGI Server

See `requirements.txt` for specific versions.

---

## � Troubleshooting

### Credentials Out of Sync
If you manually change values inside `config.py` or `.env` and it doesn't reflect your database login:
```bash
python update_admin.py
```

### "ModuleNotFoundError" on startup
```bash
pip install -r requirements.txt
```

### Database errors
```bash
rm portfolio.db
python run.py  # Recreates a fresh database
```

---

##  License

This project is open source and available under the MIT License.

---

## 👨‍💻 Credits

**Created by:** Madhesh Rasu A S  
**Tech Stack:** Flask + SQLAlchemy + Tailwind CSS + Three.js  
**Theme:** Cyberpunk Neon  

---

**Happy Coding! 🎨✨**
