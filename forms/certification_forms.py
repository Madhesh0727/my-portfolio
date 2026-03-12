from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Optional, URL

class CertificationForm(FlaskForm):
    name = StringField('Certification Name', validators=[DataRequired()])
    issuer = StringField('Issuing Organization', validators=[DataRequired()])
    date_earned = StringField('Date Earned (e.g., May 2023)', validators=[Optional()])
    url = StringField('Credential URL', validators=[Optional(), URL(require_tld=False, message="Invalid URL.")])
    description = TextAreaField('Description', validators=[Optional()])
    display_order = IntegerField('Display Order', default=0)
    submit = SubmitField('Save Certification')
