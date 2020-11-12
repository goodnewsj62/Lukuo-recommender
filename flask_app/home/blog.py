from flask import Blueprint, request, redirect, render_template, g, abort, url_for
from flask_login import current_user, login_required
from functools import wraps
from recommender import get_recommendations
from top import recommend_top
from .form import Search
from random import randrange
from flask_app.model import Movie


blog = Blueprint('blog', __name__)


def anonymous(func):
    @wraps(func)
    def anonymous_wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return func(*args, **kwargs)
        return redirect(url_for('blog.recommend_home'))
    return anonymous_wrapper


@blog.route("/home")
@anonymous
def home_page():
    return render_template('blog/index.html')


@blog.route("/home/recommend", methods=["GET", "POST"])
def recommend_home():

    context = dict()
    top_rated = recommend_top().values.tolist()
    length = len(top_rated)
    context['top rated'] = [Movie.query.filter_by(
        title=top_rated[n]).first() for n in range(length)][:10]
    context['recent'] = Movie.query.filter(
        Movie.release_date.contains('2016')).all()[:10]
    context['discover/explore movies'] = [Movie.query.filter_by(
        id=randrange(1, 3000)).first() for each in range(10)]

    if current_user.is_authenticated:
        context['recommended'] = Movie.query.filter(Movie.genres.contains(current_user.genre_a.lower(
        ) or current_user.genre_b.lower() or current_user.genre_c.lower() or current_user.genre_d.lower())).all()[:10]

    form = Search()
    result = None
    response = True
    keyword = ''

    if form.validate_on_submit():
        keyword = form.search.data
        try:
            result_final = get_recommendations(keyword)
        except:
            response = False
        names = []

        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])

        result = [Movie.query.filter_by(title=i).first() for i in names]
    return render_template('blog/home.html', response=response, context=context, keyword=keyword, results=result, form=form)


@blog.route('/details/<int:movie_id>', methods=['GET'])
def details(movie_id):

    movie = Movie.query.get(movie_id)
    if movie == None:
        return abort(404)

    result = []
    if movie:
        result_final = get_recommendations(movie.title)
        names = []
        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])

        result = [Movie.query.filter_by(title=i).first() for i in names][1:]

    return render_template('blog/movie_details.html', result=result, movie=movie)


@blog.route('/home/movies/top_rated', methods=['GET'])
def top():
    top_rated = recommend_top().values.tolist()
    length = len(top_rated)
    movie = [Movie.query.filter_by(title=top_rated[n]).first()
             for n in range(length)]

    return render_template('blog/all.html', movie=movie, title="top rated movies")


@blog.route('/home/movies/recent', methods=['GET'])
def recent():
    movie = Movie.query.filter(Movie.release_date.contains('2016')).all()
    return render_template('blog/all.html', movie=movie, title="recent movie")


@blog.route('/home/movies/discover', methods=['GET'])
def discover():
    movie = [Movie.query.filter_by(id=randrange(
        1, 3000)).first() for each in range(200)]
    return render_template('blog/all.html', movie=movie, title="discover/explore movie")


@blog.route('/home/movie/recommended', methods=['GET'])
@login_required
def recommended():
    movie = Movie.query.filter(Movie.genres.contains(current_user.genre_a.lower(
    ) or current_user.genre_b.lower() or current_user.genre_c.lower() or current_user.genre_d.lower())).all()
    return render_template('blog/all.html', movie=movie, title="recommended")


# @blog.route('/home/movie/rate', methods = ['GET'])
# def rate():
#     pass

@blog.route('/movie/genres/<string:genre>', methods=['GET'])
def movie_genre(genre):

    movie = Movie.query.filter(Movie.genres.contains(genre)).all()
    if len(movie) == 0:
        return abort(404)
    return render_template('blog/all.html', name=genre, movie=movie, title='genre')


@blog.route('/movie/genres', methods=['GET'])
def movie_genres():
    return render_template('blog/genres.html')
