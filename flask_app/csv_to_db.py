import pandas as pd
from flask import flash
import numpy as np
from sqlalchemy import create_engine, types
from config.configuration import Config
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def csv_to_movie():

    try:
        files = os.listdir(os.path.join(BASE_DIR, 'csvs/movie'))
        path = os.path.join(BASE_DIR, 'csvs', 'movie', files[0])

        dtype = {"title": str,
                 "homepage": str,
                 "cast": str,
                 "crew": str,
                 "release_date": str,
                 "original_language": str,
                 "production_countries": str,
                 "tagline": str,
                 "genres": str,
                 "overview": str,
                 "director": str,
                 "vote_count": int,
                 "vote_average": float,
                 "keywords": str,
                 "soup": str}
        data_f = pd.read_csv(path, dtype=dtype)
        data_f["rating"] = 0
        data_f.fillna(" ", inplace=True)
        # data_f = data_f.drop("Unnamed: 0", axis=1)

        # print(data_f)

        dtype = {"title": types.VARCHAR(),
                 "homepage": types.VARCHAR(),
                 "cast": types.VARCHAR(),
                 "crew": types.VARCHAR(),
                 "release_date": types.VARCHAR(),
                 "original_language": types.VARCHAR(),
                 "production_countries": types.VARCHAR(),
                 "tagline": types.VARCHAR(),
                 "genres": types.VARCHAR(),
                 "overview": types.VARCHAR(),
                 "director": types.VARCHAR(),
                 "vote_count": types.Integer(),
                 "vote_average": types.Float(),
                 "keywords": types.VARCHAR(),
                 "soup": types.VARCHAR()}

        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

        # if dtype is not None:
        #     from sqlalchemy.types import to_instance, TypeEngine
        #     for col, my_type in dtype.items():
        #         if not isinstance(to_instance(my_type), TypeEngine):
        #             raise ValueError('The type of %s is not a SQLAlchemy '
        #                              'type ' % col)

        data_f.to_sql('movie', con=engine, if_exists="append",
                      dtype=dtype, index=False)
        os.remove(path)
        flash('movie file uploaded!')
    except:
        flash('not uploaded!')
        os.remove(path)


def csv_to_music():
    try:
        files = os.listdir(os.path.join(BASE_DIR, 'csvs', 'music'))
        path = os.path.join(BASE_DIR, 'csvs', 'music', files[0])

        dtype = {
            "song_id": str,
            "title": str,
            "release": str,
            "artist_name": str,
            "year": int,
            "genres": str,
            "url": str
        }
        data_f = pd.read_csv(path, dtype=dtype)
        data_f["rating"] = 3
        data_f["producer"] = ""
        data_f["label"] = ""
        data_f["date"] = ""
        data_f["country"] = ""
        data_f["languages"] = ""
        data_f["vote_count"] = 0
        data_f.fillna(" ", inplace=True)
        # data_f = data_f.drop("Unnamed: 0", axis=1)

        # print(data_f)

        dtype = {
            "song_id": types.VARCHAR(),
            "title": types.VARCHAR(),
            "release": types.VARCHAR(),
            "artist_name": types.VARCHAR(),
            "year": types.Integer,
            "genres": types.VARCHAR(),
            "url": types.VARCHAR()
        }

        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

        # if dtype is not None:
        #     from sqlalchemy.types import to_instance, TypeEngine
        #     for col, my_type in dtype.items():
        #         if not isinstance(to_instance(my_type), TypeEngine):
        #             raise ValueError('The type of %s is not a SQLAlchemy '
        #                              'type ' % col)

        data_f.to_sql('music', con=engine, if_exists="append",
                      dtype=dtype, index=False)
        os.remove(path)
        flash('music file uploaded!')
    except:
        flash('not uploaded!')
        os.remove(path)


def csv_to_user():
    try:
        files = os.listdir(os.path.join(BASE_DIR, 'csvs', 'user_info'))
        path = os.path.join(BASE_DIR, 'csvs', 'user_info', files[0])

        dtype = {
            "user_id": str,
            "song_id": str,
            "listen_count": int
        }

        data_f = pd.read_csv(path, dtype=dtype)

        data_f.fillna(" ", inplace=True)
        # data_f = data_f.drop("Unnamed: 0", axis=1)

        print(data_f)

        dtype = {
            "user_id": types.VARCHAR(),
            "song_id": types.VARCHAR(),
            "listen_count": types.Integer
        }

        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

        # if dtype is not None:
        #     from sqlalchemy.types import to_instance, TypeEngine
        #     for col, my_type in dtype.items():
        #         if not isinstance(to_instance(my_type), TypeEngine):
        #             raise ValueError('The type of %s is not a SQLAlchemy '
        #                              'type ' % col)

        data_f.to_sql('userinfo', con=engine, if_exists="append",
                      dtype=dtype, index=False)
        os.remove(path)
        flash('user file uploaded!')
    except:
        flash('not uploaded!')
        os.remove(path)
