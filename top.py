import time
import pandas as pd
from flask_app.model import Movie
import time


def dataframe_tv(tv_data):
    df = pd.DataFrame({'title': [n.title for n in tv_data], 'vote_average': [
        n.vote_average for n in tv_data], 'vote_count': [n.vote_count for n in tv_data]})
    return df


def top_engine(tv_data=None):
    metadata = []
    if not tv_data:
        metadata = pd.read_csv('./csv/tmdb_5000_movies.csv', low_memory=False)
    else:
        metadata = dataframe_tv(tv_data)

    C = metadata['vote_average'].mean()

    m = metadata['vote_count'].quantile(0.90)

    qualified_movies = metadata.copy().loc[metadata['vote_count'] >= m]

    metadata.shape

    return qualified_movies, m, C


def recommend_top(top_engine):
    qualified_movies, m, C = top_engine

    def weighted_rating(x, m=m, C=C):
        v = x['vote_count']
        R = x['vote_average']
        return (v/(v+m) * R) + (m/(m+v) * C)

    qualified_movies['score'] = qualified_movies.apply(weighted_rating, axis=1)

    qualified_movies = qualified_movies.sort_values('score', ascending=False)
    return qualified_movies['title']


def get_popular_music():

    songmetadata = pd.read_csv('./millions_set/newsong_data.csv')

    # othersongdata = pd.read_fwf('./millions_set/10000.txt')
    othersongdata = pd.read_csv('./millions_set/10000.csv')

    # songmetadata = pd.DataFrame(songmetadata)
    othersongdata.columns = ['user_id', 'song_id', 'listen_count']

    song_df = pd.merge(othersongdata, songmetadata.drop_duplicates(
        ['song_id']), on="song_id", how="left")

    # song_df = pd.read_csv('./millions_set/songs.csv')

    song_grouped = song_df.groupby(['title']).agg({"listen_count": "count"})
    grouped_sum = song_grouped['listen_count'].sum()

    # calculating the percent share of each song in listen count
    song_grouped['percentage'] = song_grouped['listen_count'].div(
        grouped_sum)*100

    # sorting the dataset with respect to listen count
    song_grouped = song_grouped.sort_values(['listen_count'], ascending=True)
    song_df = song_df['listen_count'].astype(float)
    popular = song_grouped.sort_values(by='listen_count')

    # filtering the top ten songs in the dataset
    popularsongs = popular[-100:]

    popularsongs = pd.DataFrame(popularsongs.reset_index())
    popularsongs.sort_values('listen_count', ascending=False)

    return popularsongs


# cal = top_engine()

# start = time.time()
# print(recommend_top(cal).values.tolist())
# end = time.time()

# print("----------", (end - start))
