from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional

class ExperienceForm(FlaskForm):
    role = StringField('Role/Position', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    start_date = StringField('Start Date (e.g., Aug 2020)', validators=[Optional()])
    end_date = StringField('End Date (e.g., Present or May 2024)', validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    display_order = IntegerField('Display Order', default=0)
    submit = SubmitField('Save Experience')
