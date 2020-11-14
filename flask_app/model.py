from flask_app import db
from flask_login import UserMixin
import datetime


association_table = db.Table('association',
                             db.Column('user_id', db.Integer,
                                       db.ForeignKey('user.id')),
                             db.Column('movie_id', db.Integer,
                                       db.ForeignKey('movie.id'))
                             )


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    genre_a = db.Column(db.String(20), nullable=False, default='')
    genre_b = db.Column(db.String(20), nullable=False, default='')
    genre_c = db.Column(db.String(20), nullable=False, default='')
    genre_d = db.Column(db.String(20), nullable=False, default='')
    movie = db.relationship(
        'Movie', secondary=association_table, backref="users")


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    homepage = db.Column(db.String(30), nullable=False)
    cast = db.Column(db.String(100), nullable=False)
    crew = db.Column(db.String(300), nullable=False)
    release_date = db.Column(db.String(20), nullable=False)
    original_language = db.Column(db.String(10), nullable=False)
    production_countries = db.Column(db.String(30), nullable=False)
    tagline = db.Column(db.String(30), nullable=False)
    genres = db.Column(db.String(100), nullable=False)
    overview = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(30), nullable=False)
    vote_count = db.Column(db.Integer, nullable=False)
    vote_average = db.Column(db.Float, nullable=False)
    keywords = db.Column(db.String(50), nullable=False)
    soup = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
