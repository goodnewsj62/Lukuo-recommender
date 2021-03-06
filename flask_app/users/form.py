from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, SelectField, BooleanField
from wtforms.validators import ValidationError, EqualTo, Email, DataRequired, Length
from flask_app.model import User, Movie


class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[
                           DataRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('remember me', default=True)
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    choice = [('Action', 'action'), ('Adventure', 'adventure'), ('Comedy', 'comedy'), ('Fantasy', 'fantasy'), ('Sciencefiction', 'sciencefiction'), ('Drama', 'drama'),
              ('Romance', 'romance'), ('Animation', 'animation'), ('Family', 'family'), ('Thriller', 'thriller')]

    music_choice = [('Blues', 'blues'), ('Rock', 'rock'), ('Gospel', 'gospel'), (
        'Afro-pop', 'afro-pop'), ('Afro', 'afro'), ('Reggae', 'reggae'), ('Rap', 'rap')]

    username = StringField('Username', validators=[
                           DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(min=6)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    genre_a = SelectField('Genre A', choices=choice,
                          validators=[DataRequired()])
    genre_b = SelectField('Genre B', choices=choice,
                          validators=[DataRequired()])
    genre_c = SelectField('Genre C', choices=choice,
                          validators=[DataRequired()])
    genre_d = SelectField('Genre D', choices=choice,
                          validators=[DataRequired()])
    genre_e = SelectField('Genre A', choices=music_choice,
                          validators=[DataRequired()])
    genre_f = SelectField('Genre B', choices=music_choice,
                          validators=[DataRequired()])
    genre_g = SelectField('Genre C', choices=music_choice,
                          validators=[DataRequired()])
    genre_h = SelectField('Genre D', choices=music_choice,
                          validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('User with this email already exist')

    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username:
            raise ValidationError('User with username already exist')


class ChangePassword(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Comfirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')


class ChangeUserInfo(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(min=6)])

    submit = SubmitField('Update')
