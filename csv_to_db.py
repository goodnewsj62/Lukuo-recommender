import pandas as pd
from flask_app.model import Movie, Music, UserInfo
from flask_app import db, create_app


app = create_app()


def save_operation(name):
    with app.app_context():
        db.session.add(name)
        db.session.commit()


def to_db_movies():
    df = pd.read_csv('./newtmdb.csv')
    length = len(df)
    for i in range(length):
        print(i)
        mov = Movie(title=str(df.iloc[i, 0]), homepage=str(df.iloc[i, 1]), cast=str(df.iloc[i, 2]), crew=str(df.iloc[i, 3]), release_date=str(df.iloc[i, 4]), original_language=str(df.iloc[i, 5]), production_countries=str(df.iloc[i, 6]), tagline=str(df.iloc[i, 7]), genres=str(df.iloc[i, 8]), overview=str(df.iloc[i, 9]),
                    director=str(df.iloc[i, 10]), vote_count=str(df.iloc[i, 11]), vote_average=str(df.iloc[i, 12]), keywords=str(df.iloc[i, 13]),
                    soup=str(df.iloc[i, 14]), rating=0
                    )
        save_operation(mov)
    print('--------------------Done-----------------------')


def to_db_music():
    df = pd.read_csv('./millions_set/newsong_data.csv')
    df = df.loc[:20000]
    length = len(df)
    # i = 9237
    for i in range(length):
        # while i < len(df):
        print(i)
        mov = Music(song_id=str(df.iloc[i, 0]), title=str(df.iloc[i, 1]), release=str(df.iloc[i, 2]), artist_name=str(df.iloc[i, 3]), year=str(df.iloc[i, 4]), genres=str(df.iloc[i, 5]), url=str(df.iloc[i, 6])
                    )
        # i += 1
        save_operation(mov)
    print('--------------------Done-----------------------')


def to_db_info():
    df = pd.read_csv('./millions_set/10000.csv')
    df = df.loc[:20000]
    length = len(df)
    for i in range(length):
        print(i)
        mov = UserInfo(user_id=str(df.iloc[i, 0]), song_id=str(
            df.iloc[i, 1]), listen_count=str(df.iloc[i, 2]))
        save_operation(mov)
    print('--------------------Done-----------------------')


# to_db_movies()
# to_db_music()
to_db_info()
