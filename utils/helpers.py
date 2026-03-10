import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image
import re

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file, subfolder=''):
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        ext = original_filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        
        folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(folder, exist_ok=True)
        
        file_path = os.path.join(folder, filename)
        file.save(file_path)
        
        if ext in ['jpg', 'jpeg', 'png', 'gif']:
            optimize_image(file_path)
        
        return filename
    return None

def delete_file(filename, subfolder=''):
    if filename:
        success = True
        # Split by comma in case multiple files exist in a single string
        for fn in filename.split(','):
            fn = fn.strip()
            if not fn: continue
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder, fn)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")
                    success = False
        return success
    return False

def optimize_image(file_path, max_size=(1200, 1200), quality=85):
    try:
        img = Image.open(file_path)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (0, 0, 0))
                background.paste(img, mask=img.split()[-1])
                img = background
        
        img.save(file_path, optimize=True, quality=quality)
    except Exception as e:
        print(f"Error optimizing image: {e}")

def create_slug(title):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug