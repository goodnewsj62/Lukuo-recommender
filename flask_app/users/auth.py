from flask import Blueprint, g, abort, url_for, render_template, redirect, session, request, flash
from flask_app import bcrypt_, login_manager
from functools import wraps
from flask_login import current_user, login_required, login_user, logout_user
from flask_app.model import User
from flask_app import db
from .form import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)


def check_authenticated(func):
    @wraps(func)
    def redirect_wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return func(*args, **kwargs)
        return redirect(url_for('blog.recommend_home'))
    return redirect_wrapper


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth.route('/login', methods=['GET', 'POST'])
@check_authenticated
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
        except:
            user = User.query.filter_by(email=form.username.data).first()

        if user and bcrypt_.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            login_user(user, remember=form.remember.data)
            flash('You have logged in successfully')
            next = request.args.get('next')

            if next:
                try:
                    return redirect(next)
                except:
                    return redirect(url_for('blog.recommend_home'))
            else:
                return redirect(url_for('blog.recommend_home'))
        else:
            flash('Wrong password or username')

    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
@check_authenticated
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        password_hash = bcrypt_.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=password_hash, genre_a=form.genre_a.data, genre_b=form.genre_b.data,
                    genre_c=form.genre_c.data, genre_d=form.genre_d.data)
        db.session.add(user)
        db.session.commit()
        flash(
            f'{form.username.data.capitalize()} your account has been successfully created ')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear
    logout_user()
    flash('you have logged out successfully')
    return redirect(url_for('auth.login'))
