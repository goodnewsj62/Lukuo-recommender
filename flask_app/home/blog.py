from flask import Blueprint, request, redirect, render_template, g, abort, url_for
from flask_login import current_user, login_required
from functools import wraps
from recommender import get_recommendations
from top import recommend_top
from .form import Search
from random import randrange
from flask_app.model import Movie
from config.configuration import Config
from flask_sqlalchemy import Pagination

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

    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    movie = [Movie.query.filter_by(title=top_rated[n]).first()
             for n in range(length)]

    item = (page - 1) * Config.ITEMS_PER_PAGE
    item = movie[item: item + 20]

    pagination = Pagination(Movie.query.all(
    ), page=page, per_page=Config.ITEMS_PER_PAGE, total=len(movie), items=item)

    next_url = url_for(
        'blog.top', page=pagination.next_num) if pagination.has_next else None

    prev_url = url_for(
        'blog.top', page=pagination.prev_num) if pagination.has_prev else None

    return render_template('blog/all.html', movie=pagination.items, prev_url=prev_url, next_url=next_url, title="top rated movies")


@blog.route('/home/movies/recent', methods=['GET'])
def recent():
    page = request.args.get('page', 1, type=int)
    movie = Movie.query.filter(Movie.release_date.contains(
        '2016')).paginate(page, Config.ITEMS_PER_PAGE, True)

    next_url = url_for(
        'blog.recent', page=movie.next_num) if movie.has_next else None

    prev_url = url_for(
        'blog.recent', page=movie.prev_num) if movie.has_prev else None

    return render_template('blog/all.html', movie=movie.items, next_url=next_url, prev_url=prev_url, title="recent movie")


@blog.route('/home/movies/discover', methods=['GET'])
def discover():
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    movie = [Movie.query.filter_by(id=randrange(
        1, 3000)).first() for each in range(200)]

    # get the start index base on page number
    item = (page - 1)*(Config.ITEMS_PER_PAGE)
    end_index = item + (Config.ITEMS_PER_PAGE)

    # for page 1 [0:20] page2[20:41]
    item = movie[item: end_index]

    pagination = Pagination(Movie.query.all(), page,
                            Config.ITEMS_PER_PAGE, len(movie), item)

    prev_url = url_for(
        'blog.discover', page=pagination.prev_num) if pagination.has_prev else None

    next_url = url_for(
        'blog.discover', page=pagination.next_num) if pagination.has_next else None

    return render_template('blog/all.html', movie=pagination.items, next_url=next_url, prev_url=prev_url, title="discover/explore movie")


@blog.route('/home/movie/recommended', methods=['GET'])
@login_required
def recommended():
    page = request.args.get('page', 1, type=int)

    movie = Movie.query.filter(Movie.genres.contains(current_user.genre_a.lower(
    ) or current_user.genre_b.lower() or current_user.genre_c.lower() or current_user.genre_d.lower())).paginate(page, Config.ITEMS_PER_PAGE, True)

    prev_url = url_for('blog.recommended',
                       page=movie.prev_num) if movie.has_prev else None

    next_url = url_for('blog.recommended',
                       page=movie.next_num) if movie.has_next else None

    return render_template('blog/all.html', movie=movie.items, prev_url=prev_url, next_url=next_url, title="recommended")


# @blog.route('/home/movie/rate', methods = ['GET'])
# def rate():
#     pass

@blog.route('/movie/genres/<string:genre>', methods=['GET'])
def movie_genre(genre):
<<<<<<< HEAD

    movie = Movie.query.filter(Movie.genres.contains(genre)).all()
=======
    page = request.args.get('page', 1, type=int)

    movie = Movie.query.filter(Movie.genres.contains(
        genre)).all()

>>>>>>> FutherWorkings
    if len(movie) == 0:
        return abort(404)
    movie = Movie.query.filter(Movie.genres.contains(
        genre)).paginate(page, Config.ITEMS_PER_PAGE, True)

    prev_url = url_for('blog.movie_genre',
                       genre=genre, page=movie.prev_num) if movie.has_prev else None

    next_url = url_for('blog.movie_genre',
                       genre=genre, page=movie.next_num) if movie.has_next else None

    return render_template('blog/all.html', name=genre, movie=movie.items, prev_url=prev_url, next_url=next_url, title='genre')


@blog.route('/movie/genres', methods=['GET'])
def movie_genres():
    return render_template('blog/genres.html')
