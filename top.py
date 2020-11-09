import pandas as pd

metadata = pd.read_csv('./tmdb_5000_movies.csv', low_memory=False)

C = metadata['vote_average'].mean()


m = metadata['vote_count'].quantile(0.90)

qualified_movies = metadata.copy().loc[metadata['vote_count'] >= m]
qualified_movies.shape


metadata.shape

def weighted_rating(x,m=m,C=C):
    v = x['vote_count']
    R = x['vote_average']

    return (v/(v+m) * R) + (m/(m+v) * C)

def recommend_top():
     global  qualified_movies
     qualified_movies['score']= qualified_movies.apply(weighted_rating,axis = 1)

     qualified_movies = qualified_movies.sort_values('score',ascending=False)
     return qualified_movies['title']



# print(recommend_top())

# print(recommend_top().values.tolist())


