from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional

class EducationForm(FlaskForm):
    degree = StringField('Degree', validators=[DataRequired()])
    college = StringField('College/University', validators=[DataRequired()])
    start_date = StringField('Start Date (e.g., Aug 2020)', validators=[Optional()])
    end_date = StringField('End Date (e.g., Present or May 2024)', validators=[Optional()])
    cgpa = StringField('CGPA / Percentage', validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    display_order = IntegerField('Display Order', default=0)
    submit = SubmitField('Save Education')
