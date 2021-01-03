from sqlalchemy import create_engine
from config.configuration import Config
import pandas as pd
import sqlite3


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
df_movie = pd.read_sql_table('movie', engine)
df_music = pd.read_sql_table('music', engine)
df_user = pd.read_sql_table('userinfo', engine)
