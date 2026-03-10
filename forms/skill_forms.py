from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class SkillForm(FlaskForm):
    name = StringField('Skill Name', validators=[DataRequired(), Length(max=50)])
    category = SelectField('Category', choices=[
        ('ai-ml', 'AI/ML'),
        ('cybersecurity', 'Cybersecurity'),
        ('programming', 'Programming Languages'),
        ('tools', 'Tools & Technologies'),
        ('soft', 'Soft Skills')
    ], validators=[DataRequired()])
    level = IntegerField('Proficiency Level (0-100)', validators=[Optional(), NumberRange(min=0, max=100)], default=80)
    icon = StringField('Icon Class (FontAwesome)', validators=[Optional(), Length(max=50)])
    display_order = IntegerField('Display Order', validators=[Optional()], default=0)
    submit = SubmitField('Save Skill')