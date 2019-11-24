from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL
from db import getSizeOfURL

class UrlForm(FlaskForm):
    urlFromUser = StringField('Url',
    validators=[DataRequired(), URL(require_tld=True, message='URL Not Valid')])

    submit = SubmitField('Create short URL')
