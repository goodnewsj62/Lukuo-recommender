import os
from flask import Blueprint, request, redirect, render_template, g, abort, url_for, session
from flask_cors import cross_origin
from flask_login import current_user, login_required
from functools import wraps
from recommender import Recommender
from top import recommend_top, top_engine, get_popular_music
from .form import Search
import random
from flask_app import db
from flask_app.model import Movie, Music, User
from config.configuration import Config
from flask_sqlalchemy import Pagination
import difflib


blog = Blueprint('blog', __name__)


@blog.before_app_request
def get_language():
    ip = None
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
        ip = ip.split(',')
        ip = ip[0]

    session['ip'] = ip


def anonymous(func):
    @wraps(func)
    def anonymous_wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return func(*args, **kwargs)
        return redirect(url_for('blog.recommend_home'))
    return anonymous_wrapper


@blog.route("/")
@blog.route("/home")
@anonymous
def home_page():
    return render_template('blog/index.html')


@blog.route("/home/recommend", methods=["GET", "POST"])
def recommend_home():

    context = dict()
    type_ = "movie"

    calculations = top_engine()
    top_rated = recommend_top(calculations).values.tolist()
    context['top rated'] = [Movie.query.filter_by(
        title=top_rated[n]).first() for n in range(10)]

    context['recent'] = Movie.query.filter(
        Movie.release_date.contains('2016'))[:10]

    context['discover/explore movies'] = [Movie.query.filter_by(
        id=random.randrange(1, 3000)).first() for each in range(10)]

    if current_user.is_authenticated:
        context['recommended'] = Movie.query.filter(Movie.genres.contains(current_user.genre_a.lower(
        ) or current_user.genre_b.lower() or current_user.genre_c.lower() or current_user.genre_d.lower()))[:10]

    form = Search()
    result = None
    response = True
    keyword = None

    if form.validate_on_submit():
        keyword = form.search.data
        recommend = Recommender(type_)
        result_final = ''
        try:
            result_final = recommend.get_recommendations(keyword)
        except:
            response = False
        names = []

        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])

        result = Movie.query.filter(Movie.title.in_(names)).all()

    return render_template('blog/home.html', response=response, context=context, keyword=keyword, results=result, form=form, viewtype=type_)


@blog.route('/details/<int:id>', methods=['GET'])
def details_movie(id):

    movie = Movie.query.get(id)
    if movie == None:
        return abort(404)

    result = []
    if movie:
        recommend = Recommender("movie")
        result_final = recommend.get_recommendations(movie.title)
        names = []
        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])

        result = [Movie.query.filter_by(title=i).first() for i in names][1:]

    return render_template('blog/movie_details.html', result=result, movie=movie, viewtype='movie')


@blog.route('/home/movies/top_rated', methods=['GET'])
def top_movie():
    calculations = top_engine()
    top_rated = recommend_top(calculations).values.tolist()
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
        'blog.top_movie', page=pagination.next_num) if pagination.has_next else None

    prev_url = url_for(
        'blog.top_movie', page=pagination.prev_num) if pagination.has_prev else None

    return render_template('blog/all.html', movie=pagination.items, prev_url=prev_url, next_url=next_url, title="top rated movies", viewtype='movie')


@blog.route('/home/movies/recent', methods=['GET'])
def recent_movie():
    page = request.args.get('page', 1, type=int)
    movie = Movie.query.filter(Movie.release_date.contains(
        '2016')).paginate(page, Config.ITEMS_PER_PAGE, True)

    next_url = url_for(
        'blog.recent_movie', page=movie.next_num) if movie.has_next else None

    prev_url = url_for(
        'blog.recent_movie', page=movie.prev_num) if movie.has_prev else None

    return render_template('blog/all.html', movie=movie.items, next_url=next_url, prev_url=prev_url, title="recent movie", viewtype='movie')


@blog.route('/home/movies/discover', methods=['GET'])
def discover_movie():
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    movie = [Movie.query.filter_by(id=random.randrange(
        1, 3000)).first() for each in range(200)]

    # get the start index base on page number
    item = (page - 1)*(Config.ITEMS_PER_PAGE)
    end_index = item + (Config.ITEMS_PER_PAGE)

    # for page 1 [0:20] page2[20:41]
    item = movie[item: end_index]

    pagination = Pagination(Movie.query.all(), page,
                            Config.ITEMS_PER_PAGE, len(movie), item)

    prev_url = url_for(
        'blog.discover_movie', page=pagination.prev_num) if pagination.has_prev else None

    next_url = url_for(
        'blog.discover_movie', page=pagination.next_num) if pagination.has_next else None

    return render_template('blog/all.html', movie=pagination.items, next_url=next_url, prev_url=prev_url, title="discover/explore movie", viewtype='movie')


@blog.route('/home/movie/recommended', methods=['GET'])
@login_required
def recommended_movie():
    page = request.args.get('page', 1, type=int)

    movie = Movie.query.filter(Movie.genres.contains(current_user.genre_a.lower(
    ) or current_user.genre_b.lower() or current_user.genre_c.lower() or current_user.genre_d.lower())).paginate(page, Config.ITEMS_PER_PAGE, True)

    prev_url = url_for('blog.recommended_movie',
                       page=movie.prev_num) if movie.has_prev else None

    next_url = url_for('blog.recommended_movie',
                       page=movie.next_num) if movie.has_next else None

    return render_template('blog/all.html', movie=movie.items, prev_url=prev_url, next_url=next_url, viewtype='movie', title="recommended")


# @blog.route('/home/movie/rate', methods = ['GET'])
# def rate():
#     pass

@blog.route('/movie/genres/<string:genre>', methods=['GET'])
def genre_movie(genre):
    page = request.args.get('page', 1, type=int)

    movie = Movie.query.filter(Movie.genres.contains(
        genre)).all()

    if len(movie) == 0:
        return abort(404)
    movie = Movie.query.filter(Movie.genres.contains(
        genre)).paginate(page, Config.ITEMS_PER_PAGE, True)

    prev_url = url_for('blog.genre_movie',
                       genre=genre, page=movie.prev_num) if movie.has_prev else None

    next_url = url_for('blog.genre_movie',
                       genre=genre, page=movie.next_num) if movie.has_next else None

    return render_template('blog/all.html', name=genre, movie=movie.items, prev_url=prev_url, next_url=next_url, title='genre', viewtype='movie')


@blog.route('/movie/genres', methods=['GET'])
def genres_movie():
    return render_template('blog/genres.html', viewtype='movie')

# --------------------------music-----------------------


@blog.route('/home/music', methods=['GET', 'POST'])
def music_recommend():
    context = dict()

    popular = get_popular_music()
    popular_songs = []

    for n in range(10):
        popular_songs.append(popular.iloc[n][0])

    context['top rated'] = Music.query.filter(
        Music.title.in_(popular_songs))[:10]

    context['recent'] = Music.query.filter(
        Music.year.contains(2010 or 2011))[:10]

    context['discover/explore music'] = [Music.query.filter_by(
        id=random.randrange(1, 10000)).first() for each in range(10)]

    if current_user.is_authenticated:
        context['recommended'] = Music.query.filter(Music.genres.contains(current_user.genre_e.lower(
        ) or current_user.genre_f.lower() or current_user.genre_g.lower() or current_user.genre_h.lower()))[:10]

    type_ = "music"
    form = Search()
    result = None
    response = True
    keyword = None

    if form.validate_on_submit():

        keyword = form.search.data

        common = difflib.get_close_matches(
            keyword, [n.title for n in Music.query.all()], 1)
        try:
            titlesim = common[0]
        except:
            titlesim = keyword

        hold = False

        try:
            hold = Music.query.filter_by(title=titlesim).first().id
        except:
            response = False

        if hold:

            #  due to range the recommender can handle we make sure the no of data items(rows in csv) is just 5000

            similarities = Recommender(type_, hold, (hold + 5000))

            results = similarities.get_recommendations(keyword)

            hold_results = list()

            for each in range(len(results)):
                hold_results.append(results[each])

            result = Music.query.filter(
                Music.id.in_(hold_results)).all()

    return render_template('blog/home.html', results=result, viewtype=type_, context=context, form=form, keyword=keyword, response=response)


@blog.route('/music/details/<int:id>')
def details_music(id):
    music = Music.query.get(id)

    if music == None:
        return abort(404)

    result = []
    if music:
        recommend = Recommender("music", id, (id + 5000))
        result_final = recommend.get_recommendations(music.title)

        result = [Music.query.filter_by(
            id=result_final[i]).first() for i in range(10)][1:]

    return render_template('blog/music_details.html', result=result, music=music, viewtype='music')


@blog.route('/home/music/top_rated', methods=['GET'])
def top_music():
    popular = get_popular_music()
    top_rated = []

    for n in range(10):
        top_rated.append(popular.iloc[n][0])

    length = len(top_rated)

    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    music = [Music.query.filter_by(title=top_rated[n]).first()
             for n in range(length)]

    item = (page - 1) * Config.ITEMS_PER_PAGE
    item = music[item: item + 20]

    pagination = Pagination(Music.query.all(
    ), page=page, per_page=Config.ITEMS_PER_PAGE, total=len(music), items=item)

    next_url = url_for(
        'blog.top_music', page=pagination.next_num) if pagination.has_next else None

    prev_url = url_for(
        'blog.top_music', page=pagination.prev_num) if pagination.has_prev else None

    return render_template('blog/all.html', music=pagination.items, prev_url=prev_url, next_url=next_url, viewtype='music', title="top rated music")


@blog.route('/home/music/recent', methods=['GET'])
def recent_music():
    page = request.args.get('page', 1, type=int)
    music = Music.query.filter(Music.year.contains(
        2010 or 2011)).paginate(page, Config.ITEMS_PER_PAGE, True)

    next_url = url_for(
        'blog.recent_music', page=music.next_num) if music.has_next else None

    prev_url = url_for(
        'blog.recent_music', page=music.prev_num) if music.has_prev else None

    return render_template('blog/all.html', music=music.items, next_url=next_url, prev_url=prev_url, title="recent music", viewtype='music')


@blog.route('/home/music/discover', methods=['GET'])
def discover_music():
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    music = [Music.query.filter_by(id=random.randrange(
        1, 10000)).first() for each in range(200)]

    # get the start index base on page number
    item = (page - 1)*(Config.ITEMS_PER_PAGE)
    end_index = item + (Config.ITEMS_PER_PAGE)

    # for page 1 [0:20] page2[20:41]
    item = music[item: end_index]

    pagination = Pagination(Music.query.all(), page,
                            Config.ITEMS_PER_PAGE, len(music), item)

    prev_url = url_for(
        'blog.discover_music', page=pagination.prev_num) if pagination.has_prev else None

    next_url = url_for(
        'blog.discover_music', page=pagination.next_num) if pagination.has_next else None

    return render_template('blog/all.html', music=pagination.items, next_url=next_url, viewtype='music', prev_url=prev_url, title="discover/explore music")


@blog.route('/home/music/recommended', methods=['GET'])
@login_required
def recommended_music():
    page = request.args.get('page', 1, type=int)

    music = Music.query.filter(Music.genres.contains(current_user.genre_e.lower(
    ) or current_user.genre_f.lower() or current_user.genre_g.lower() or current_user.genre_h.lower())).paginate(page, Config.ITEMS_PER_PAGE, True)

    prev_url = url_for('blog.recommended_music',
                       page=music.prev_num) if music.has_prev else None

    next_url = url_for('blog.recommended_music',
                       page=music.next_num) if music.has_next else None

    return render_template('blog/all.html', music=music.items, prev_url=prev_url, next_url=next_url, viewtype='music', title="recommended music")


@blog.route('/music/genres/<string:genre>', methods=['GET'])
def genre_music(genre):
    page = request.args.get('page', 1, type=int)

    music = Music.query.filter(Music.genres.contains(
        genre)).all()

    if len(music) == 0:
        return abort(404)
    music = Music.query.filter(Music.genres.contains(
        genre)).paginate(page, Config.ITEMS_PER_PAGE, True)

    prev_url = url_for('blog.genre_music',
                       genre=genre, page=music.prev_num) if music.has_prev else None

    next_url = url_for('blog.genre_music',
                       genre=genre, page=music.next_num) if music.has_next else None

    return render_template('blog/all.html', name=genre, music=music.items, prev_url=prev_url, next_url=next_url, viewtype='music', title='music genre')


@blog.route('/music/genres', methods=['GET'])
def genres_music():
    return render_template('blog/genres.html', viewtype='music')


# ----------------------tvseries---------------------

@blog.route('/home/tv', methods=['GET', 'POST'])
def tv_recommend():
    type_ = 'tv'

    all_data = Movie.query.filter(Movie.genres.contains('tv')).all()

    context = dict()

    calculations = top_engine(all_data)
    top = recommend_top(calculations).values.tolist()

    context['top rated'] = [Movie.query.filter_by(
        title=top[each]).first() for each in range(len(top))]

    context['recent'] = [n for n in all_data if n.release_date[:4]
                         == "2013" or n.release_date[:4] == "2012"]

    context['discover/explore movies'] = [
        all_data[random.randrange(0, 4)] for n in range(4)]

    if current_user.is_authenticated:
        recomm = Movie.query.filter(Movie.genres.contains(current_user.genre_a.lower(
        ) or current_user.genre_b.lower() or current_user.genre_c.lower() or current_user.genre_d.lower())).all()
        context['recommended'] = [
            each for each in recomm if "tvmovie" in each.genres]

    form = Search()
    result = None
    response = True
    keyword = None

    if form.validate_on_submit():
        keyword = form.search.data

        recommend = Recommender(recom_type=type_, tv_data=all_data)

        result_final = ''
        try:
            result_final = recommend.get_recommendations(keyword)
        except:
            response = False
        names = []

        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])

        result = Movie.query.filter(Movie.title.in_(names)).all()

    return render_template('blog/home.html', response=response, context=context, keyword=keyword, results=result, form=form, viewtype=type_)


@blog.route('/tv/details/<int:id>', methods=['GET'])
def details_tv(id):

    tv = Movie.query.get(id)
    all_data = Movie.query.filter(Movie.genres.contains('tv')).all()

    if tv == None or not all_data:
        return abort(404)

    result = []
    if tv:
        recommend = Recommender(recom_type='tv', tv_data=all_data)
        result_final = recommend.get_recommendations(tv.title)
        names = []
        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])

        result = [Movie.query.filter_by(title=i).first() for i in names][1:]

    return render_template('blog/movie_details.html', result=result, movie=tv, viewtype='tv')


@blog.route('/home/tv/top_rated', methods=['GET'])
def top_tv():
    all_data = Movie.query.filter(Movie.genres.contains('tv')).all()

    calculations = top_engine(all_data)
    top_rated = recommend_top(calculations).values.tolist()
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
        'blog.top_tv', page=pagination.next_num) if pagination.has_next else None

    prev_url = url_for(
        'blog.top_tv', page=pagination.prev_num) if pagination.has_prev else None

    return render_template('blog/all.html', movie=pagination.items, prev_url=prev_url, viewtype='tv', next_url=next_url, title="top rated series")


@blog.route('/home/tv/recent', methods=['GET'])
def recent_tv():
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    movie = Movie.query.filter(Movie.release_date.contains(
        '2012' or '2013')).all()

    movie = [n for n in movie if "tvmovie" in n.genres]

    item = (page - 1) * Config.ITEMS_PER_PAGE
    item = movie[item: item + 20]

    pagination = Pagination(Movie.query.all(
    ), page=page, per_page=Config.ITEMS_PER_PAGE, total=len(movie), items=item)

    next_url = url_for(
        'blog.recent_tv', page=pagination.next_num) if pagination.has_next else None

    prev_url = url_for(
        'blog.recent_tv', page=pagination.prev_num) if pagination.has_prev else None

    return render_template('blog/all.html', movie=pagination.items, next_url=next_url, prev_url=prev_url, viewtype='tv', title="recent movie series")


@blog.route('/home/tv/discover', methods=['GET'])
def discover_tv():
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    all_data = Movie.query.filter(Movie.genres.contains('tv')).all()

    movie = [all_data[random.randint(0, 4)] for each in range(5)]

    # get the start index base on page number
    item = (page - 1)*(Config.ITEMS_PER_PAGE)
    end_index = item + (Config.ITEMS_PER_PAGE)

    # for page 1 [0:20] page2[20:41]
    item = movie[item: end_index]

    pagination = Pagination(Movie.query.all(), page,
                            Config.ITEMS_PER_PAGE, len(movie), item)

    prev_url = url_for(
        'blog.discover_tv', page=pagination.prev_num) if pagination.has_prev else None

    next_url = url_for(
        'blog.discover_tv', page=pagination.next_num) if pagination.has_next else None

    return render_template('blog/all.html', movie=pagination.items, next_url=next_url, prev_url=prev_url, viewtype='tv', title="discover/explore tv series")


@blog.route('/home/tv/recommended', methods=['GET'])
@login_required
def recommended_tv():
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    recomm = Movie.query.filter(Movie.genres.contains(current_user.genre_a.lower(
    ) or current_user.genre_b.lower() or current_user.genre_c.lower() or current_user.genre_d.lower())).all()
    all_data = [each for each in recomm if "tvmovie" in each.genres]

    # get the start index base on page number
    item = (page - 1)*(Config.ITEMS_PER_PAGE)
    end_index = item + (Config.ITEMS_PER_PAGE)

    # for page 1 [0:20] page2[20:41]
    item = all_data[item: end_index]

    movie = Pagination(Movie.query.all(), page,
                       Config.ITEMS_PER_PAGE, len(all_data), item)

    prev_url = url_for('blog.recommended_tv',
                       page=movie.prev_num) if movie.has_prev else None

    next_url = url_for('blog.recommended_tv',
                       page=movie.next_num) if movie.has_next else None

    return render_template('blog/all.html', movie=movie.items, prev_url=prev_url, next_url=next_url, viewtype='tv', title="recommended for series")


@blog.route('/tv/genres/<string:genre>', methods=['GET'])
def genre_tv(genre):
    try:
        page = request.args.get('page', 1, type=int)
    except:
        page = 1

    # get the start index base on page number

    all_data = Movie.query.filter(Movie.genres.contains(
        genre)).all()

    movie = [each for each in all_data if "tvmovie" in each.genres]
    if len(all_data) == 0 or len(movie) == 0:
        return abort(404)

    item = (page - 1)*(Config.ITEMS_PER_PAGE)
    end_index = item + (Config.ITEMS_PER_PAGE)

    # for page 1 [0:20] page2[20:41]
    item = movie[item:end_index]

    movie = Pagination(Movie.query.all(), page,
                       Config.ITEMS_PER_PAGE, len(movie), item)

    prev_url = url_for('blog.genre_tv',
                       genre=genre, page=movie.prev_num) if movie.has_prev else None

    next_url = url_for('blog.genre_tv',
                       genre=genre, page=movie.next_num) if movie.has_next else None

    return render_template('blog/all.html', name=genre, movie=movie.items, prev_url=prev_url, next_url=next_url, viewtype='tv', title='genre for series')


@blog.route('/tv/genres', methods=['GET'])
def genres_tv():
    return render_template('blog/genres.html', viewtype='tv')


# ----------------------------overall-------------------------

@blog.route('/rating', methods=['GET', 'POST'])
@cross_origin()
def rate_movie():

    if request.method == 'POST':

        # remove \n\r and  ' ' if exists
        title = request.form['title'].split()
        if len(title) == 1:
            title = title[0]
        else:
            title = request.form['title']
        username = request.form['username'].split()

        user = User.query.filter_by(username=username[0]).first()
        movie = Movie.query.filter_by(title=title).first()
        music = Music.query.filter_by(song_id=title).first()

        if music == [] or music == None:
            rating_ = movie.rating
            movie.users.append(user)

            movie.rating = (int(request.form['level']) + rating_)
            user.movie.append(movie)

            db.session.add(movie)
            db.session.add(user)
            db.session.commit()
        else:
            rating_ = music.vote_count

            music.user_ids.append(user)

            music.vote_count = (int(request.form['level']) + rating_)
            user.music.append(music)

            db.session.add(music)
            db.session.add(user)
            db.session.commit()

    return 'Done'


@blog.route('/movie/ratings', methods=['GET'])
def ratings():
    user = []

    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(username=current_user.username).first()
    user = user.movie

    no_of_movies = len(user)
    item = (page - 1)*(Config.ITEMS_PER_PAGE)
    end_index = item + (Config.ITEMS_PER_PAGE)

    # for page 1 [0:20] page2[20:41]
    item = user[item:end_index]

    movie = Pagination(Movie.query.all(), page,
                       Config.ITEMS_PER_PAGE, len(user), item)

    prev_url = url_for('blog.genre_tv',
                       page=movie.prev_num) if movie.has_prev else None

    next_url = url_for('blog.genre_tv',
                       page=movie.next_num) if movie.has_next else None

    return render_template('blog/ratings.html', movie=movie.items, prev_url=prev_url,
                           next_url=next_url, no=no_of_movies, viewtype="movie")


@blog.route('/music/ratings', methods=['GET'])
def music_ratings():
    user = []

    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(username=current_user.username).first()
    user = user.music

    no_of_music = len(user)
    item = (page - 1)*(Config.ITEMS_PER_PAGE)
    end_index = item + (Config.ITEMS_PER_PAGE)

    # for page 1 [0:20] page2[20:41]
    item = user[item:end_index]

    music = Pagination(Music.query.all(), page,
                       Config.ITEMS_PER_PAGE, len(user), item)

    prev_url = url_for('blog.genre_tv',
                       page=music.prev_num) if music.has_prev else None

    next_url = url_for('blog.genre_tv',
                       page=music.next_num) if music.has_next else None

    return render_template('blog/ratings.html', music=music.items, prev_url=prev_url,
                           next_url=next_url, no=no_of_music, viewtype='music')


@blog.route('/tv/ratings', methods=['GET'])
def tv_ratings():
    user = []

    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(username=current_user.username).first()
    user = user.movie
    user = [each for each in user if "tvmovie" in each.genres]

    no_of_movies = len(user)
    item = (page - 1)*(Config.ITEMS_PER_PAGE)
    end_index = item + (Config.ITEMS_PER_PAGE)

    # for page 1 [0:20] page2[20:41]
    item = user[item:end_index]

    movie = Pagination(Movie.query.all(), page,
                       Config.ITEMS_PER_PAGE, len(user), item)

    prev_url = url_for('blog.genre_tv',
                       page=movie.prev_num) if movie.has_prev else None

    next_url = url_for('blog.genre_tv',
                       page=movie.next_num) if movie.has_next else None

    return render_template('blog/ratings.html', movie=movie.items, prev_url=prev_url,
                           next_url=next_url, no=no_of_movies, viewtype="tv")
