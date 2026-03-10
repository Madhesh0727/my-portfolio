from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import Optional, Email, URL, Length

class SettingsForm(FlaskForm):
    site_name = StringField('Site Text (Navbar Logo)', validators=[Optional(), Length(max=100)])
    owner_name = StringField('Owner Name (Hero Headline)', validators=[Optional(), Length(max=100)])
    contact_text = TextAreaField('Contact CTA Text (Bottom of page)', validators=[Optional(), Length(max=500)])
    contact_page_text = TextAreaField('Contact Page Intro text', validators=[Optional(), Length(max=1000)])
    bio = TextAreaField('Who I Am (Bio)', validators=[Optional(), Length(max=1000)])
    what_i_do = TextAreaField('What I Do (One item per line)', validators=[Optional(), Length(max=2000)])
    tagline = StringField('Tagline', validators=[Optional(), Length(max=200)])
    profile_image = FileField('Profile Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    theme_color = StringField('Theme Color (hex)', validators=[Optional(), Length(max=7)], default='#00ff00')
    
    # Admin Security
    admin_username = StringField('Admin Username', validators=[Optional(), Length(min=3, max=50)])
    new_password = PasswordField('New Admin Password (leave blank to keep current)', validators=[Optional(), Length(min=6)])
    
    # Social links
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), URL()])
    twitter_url = StringField('Twitter URL', validators=[Optional(), URL()])
    instagram_url = StringField('Instagram URL', validators=[Optional(), URL()])
    whatsapp_url = StringField('WhatsApp URL', validators=[Optional(), URL()])
    email = StringField('Email', validators=[Optional(), Email()])
    
    # Files
    resume = FileField('Resume (PDF)', validators=[
        Optional(),
        FileAllowed(['pdf'], 'PDF only!')
    ])
    
    submit = SubmitField('Save Settings')