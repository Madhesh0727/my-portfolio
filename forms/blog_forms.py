from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class BlogPostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(max=200)])
    excerpt = StringField('Excerpt (short summary)', validators=[Optional(), Length(max=300)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('AI/ML', 'AI/ML'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Tutorial', 'Tutorial'),
        ('News', 'News'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    image = MultipleFileField('Featured Images/Videos', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'webm', 'ogg', 'mov'], 'Images and Videos only!')
    ])
    published = BooleanField('Publish immediately')
    submit = SubmitField('Save Post')