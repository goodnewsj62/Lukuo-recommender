from flask import Blueprint,request,redirect,render_template,g,abort,url_for
from flask_login import current_user
from functools import wraps
from recommender import get_recommendations
from top import recommend_top
from .form import Search
from random import randrange
from flask_app.model import Movie

blog = Blueprint('blog',__name__)


def anonymous(func):
    @wraps(func)
    def anonymous_wrapper(*args,**kwargs):
        if not current_user.is_authenticated:
            return func(*args,**kwargs)
        return redirect(url_for('blog.recommend_home'))
    return anonymous_wrapper

@blog.route("/home")
@anonymous
def home_page():
    return  render_template('blog/index.html')


@blog.route("/home/recommend", methods= ["GET","POST"])
def recommend_home():
    movie = Movie.query.all()

    # user = User.query.filter_by(username = current_user)
    recommended = None
    # if current_user.is_authenticated:
    #     if len(user.movie) > 10:
    #         movie_id = user.movie

    top_rated = recommend_top().values.tolist()
    length = len(top_rated)
    top = [Movie.query.filter_by(title=top_rated[n]).first() for n in range(length)]
    recent = Movie.query.filter(Movie.release_date.contains('2016')).all()

    form = Search()
    result = None
    response = True
    keyword = ''

    random_ = [Movie.query.filter_by(id = randrange(1,3000)).first() for each in range(10)]
    if  form.validate_on_submit():
        keyword = form.search.data
        try:
            result_final = get_recommendations(keyword)
        except:
            response = False
        names = []

        rating = []
        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])
            rating.append(result_final.iloc[i][2])

        result = [Movie.query.filter_by(title = i).first() for i in names]
        # ratings = [trunc(float(n)/1.5) for n in rating]
        # for each in genre:
        #     each = each.translate(each.maketrans("", "", '""[],'))
        #     each = each.translate(each.maketrans("", "", "'"))
        #     first, *args, third = each.split()
        #
        #     if len(args) > 0:
        #         genres.append((first, args[0], third))
        #     else:
        #         genres.append((first, third))


    return render_template('blog/home.html', top = top[:10],response = response
                           ,keyword = keyword,recent = recent[:10], results = result,form = form, random = random_)


