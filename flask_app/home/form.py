from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo


class Search(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField('Search')


class Files(FlaskForm):
    file = FileField(validators=[FileRequired(
    ), FileAllowed(['csv', 'txt'], 'Csv files')])
    options = SelectField('type', validators=[DataRequired()], choices=[
                          ('movie', 'movie'), ('music', 'music'), ('user', 'user')])
    submit = SubmitField('Upload')


# class Search2(FlaskForm):
#     music_search = StringField('search', validators = [DataRequired()])
#     submit = SubmitField('Search')
