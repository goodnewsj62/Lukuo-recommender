from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,EqualTo


class Search(FlaskForm):
    search = StringField('search', validators = [DataRequired()])
    submit = SubmitField('Search')