import pandas as pd
from flask_app.database import engine
from flask_app.model import Movie
from flask_app.database import db_session



df = pd.read_csv('./newtmdb.csv' )

length = len(df)


for i in range(length):
        print(i)
        mov = Movie(title = str(df.iloc[i,0]), homepage = str(df.iloc[i,1]) ,cast = str(df.iloc[i,2])
                , crew = str(df.iloc[i,3]) , release_date = str(df.iloc[i,4]) ,original_language = str(df.iloc[i,5])
                , production_countries = str(df.iloc[i,6]),tagline =str(df.iloc[i,7])
                ,genres = str(df.iloc[i,8]) ,overview =str(df.iloc[i,9]),
                director = str(df.iloc[i,10]), vote_count =str(df.iloc[i,11])
                ,vote_average = str(df.iloc[i,12]) , keywords =str(df.iloc[i,13]),
                soup =str(df.iloc[i,14]), rating = 0
                )
        db_session.add(mov)
        db_session.commit()


