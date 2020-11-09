from flask_app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String,Table,ForeignKey
from flask_login import UserMixin
import datetime


association_table = Table('association', Base.metadata,
                          Column('user_id',Integer,ForeignKey('user.id')),
                          Column('movie_id',Integer,ForeignKey('movie.id'))
                          )

class User(Base,UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True,nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    genre_a = Column(String(20),nullable=False, default='')
    genre_b = Column(String(20),nullable=False, default='')
    genre_c = Column(String(20),nullable=False, default='')
    genre_d = Column(String(20),nullable=False, default='')
    movie = relationship('Movie', secondary =association_table, backref = "users")

class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer,primary_key=True)
    title = Column(String(30), nullable=False)
    homepage = Column(String(30), nullable=False)
    cast = Column(String(100), nullable=False)
    crew = Column(String(300), nullable=False)
    release_date = Column(String(20), nullable=False)
    original_language = Column(String(10), nullable=False)
    production_countries = Column(String(30), nullable=False)
    tagline = Column(String(30), nullable=False)
    genres = Column(String(100), nullable=False)
    overview = Column(String(100), nullable=False)
    director = Column(String(30), nullable=False)
    vote_count = Column(String(15), nullable=False)
    vote_average =Column(String(15), nullable=False)
    keywords = Column(String(50), nullable=False)
    soup = Column(String(100), nullable=False)
    rating = Column(Integer,nullable=False, default =0)


