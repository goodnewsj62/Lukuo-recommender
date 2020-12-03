import pandas as pd
import random


def keep_columns():
    f = pd.read_csv("./tmdb.csv")
    keep_col = ["title",
                "homepage",
                "cast",
                "crew",
                "release_date",
                "original_language",
                "production_countries",
                "tagline",
                "genres",
                "overview",
                "director",
                "vote_count",
                "vote_average",
                "keywords",
                "soup"]
    new_f = f[keep_col]
    new_f.to_csv("newtmdb.csv", index=False)


def txt_to_csv():
    read_data = pd.read_fwf('./millions_set/10000.txt')
    read_data.columns = ['user_id', 'song_id', 'listen_count']
    read_data.to_csv('./millions_set/10000.csv', index=None)


def random_genre():
    file = pd.read_csv('./millions_set/song_data.csv')
    list_ = []
    for n in range(len(file)):
        list_.append(random.choice(
            ['blues', 'rock', 'gospel', 'afro-pop', 'reggae', 'afro', 'rap']))
    return list_


def add_new_columns():
    df = pd.read_csv('./millions_set/song_data.csv')
    genres = random_genre()
    url = ["" for i in range(len(df))]
    df["genres"] = genres
    df['url'] = url

    df.to_csv('./millions_set/newsong_data.csv', index=False)


def merge_to_csv():
    df = pd.read_csv('./millions_set/newsong_data.csv')
    df1 = pd.read_csv('./millions_set/10000.csv')
    df1.columns = ['user_id', 'song_id', 'listen_count']

    df = pd.DataFrame(df)

    song_df = pd.merge(df1, df.drop_duplicates(
        ['song_id']), on="song_id", how="left")

    song_df.to_csv('./millions_set/songs.csv', index=False)


def drop_duplicate():
    song = pd.read_csv('./millions_set/songs.csv')

    song.drop_duplicates(keep=False, inplace=True)
    # sorting by first name
    song.sort_values("title", inplace=True)

    # dropping duplicate values

    song.to_csv('./millions_set/songs.csv', index=False)


def cut_csv(up_to, path, save_path):
    df = pd.read_csv(path)
    df = df.loc[:up_to]
    df.to_csv(save_path, index=False)


cut_csv(20000, './millions_set/10000.csv',
        './millions_set/10000.csv')


# drop_duplicate()


# add_new_columns()
# merge_to_csv()
