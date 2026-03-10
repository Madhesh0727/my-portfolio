from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Short Description', validators=[DataRequired(), Length(max=500)])
    long_description = TextAreaField('Detailed Description', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('AI/ML', 'AI/ML'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Web Development', 'Web Development'),
        ('Mobile App', 'Mobile App'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    image = MultipleFileField('Project Images', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'svg'], 'Images only!')
    ])
    tech_stack = StringField('Technologies (comma separated)', validators=[Optional(), Length(max=500)])
    github_link = StringField('GitHub URL', validators=[Optional(), URL()])
    demo_link = StringField('Live Demo URL', validators=[Optional(), URL()])
    featured = BooleanField('Featured Project')
    submit = SubmitField('Save Project')