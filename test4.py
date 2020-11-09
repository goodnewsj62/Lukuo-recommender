import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

from scipy.spatial.distance import cosine, correlation
from surprise import Reader, Dataset, SVD, NormalPredictor, BaselineOnly, KNNBasic, NMF
from surprise.model_selection import cross_validate, KFold ,GridSearchCV , RandomizedSearchCV


# credits = pd.read_csv("./tmdb_5000_credits.csv")
movies = pd.read_csv("./tmdb.csv")


# credits.columns = ['id','cast','crew','genres']
# movies= movies.merge(credits,on='id')



features = ['genres']


#coverting strings to usable objects
for feature in features:
        movies[feature] = pd.DataFrame(movies[feature])



def get_director(inp):
    for i in inp:
        if 'job'in i:
            if i['job'] == 'Director':
                return i['name']
    return np.nan


def get_list(inp):
    if isinstance(inp,list):
        names = [i['name'] for i in inp]
        if len(names) > 3:
            names = names[:3]
        return  names
    return []




#since we have gotten director from crew we remove crew
features = ['genres']

for feature in features:
    movies[feature] = movies[feature].apply(get_list)

movies['genres'].head(3)


#remove spaces so we dont confuse the machine

def clean_data(x):
    if isinstance(x,list):
        return [str.lower(i.replace(" ","")) for i in x]
    else:
        #check if director exist
        if isinstance(x,str):
            return str.lower(x.replace(" ",""))
        else:
            return ''


#apply clean data

features = ['genres']

for feature in features:
    movies[feature] = movies[feature].apply(clean_data)

def create_soup(x):
    return ' '.join(x['genres'])

movies['soup'] = movies.apply(create_soup, axis = 1)
plots = movies['soup']

# cv = CountVectorizer()
# count_matrix = cv.fit_transform(movie["combined_features"])
# cosine_sim = cosine_similarity(count_matrix)
tfidf = TfidfVectorizer(stop_words = 'english' , max_df = 4 , min_df= 1)

plots = plots.fillna('')


tfidf_matrix = tfidf.fit_transform(plots)

cos_similar = linear_kernel(tfidf_matrix , tfidf_matrix)
cos_similar.shape


indices = pd.Series(movies.index , index = movies['genres']).drop_duplicates()

def get_movies(title):
    idx = indices["['fantasy', 'action']"]
    similar = list(enumerate(cos_similar[idx]))
    similar = sorted(similar, key = lambda x: x[1] , reverse = True)
    similar = similar[:11]
    indic = []
    for i in similar:
        indic.append(i[0])
    title_ = movies['title'].iloc[indic]
    return_df = pd.DataFrame(columns=['Title'])
    return_df['Title'] = title_
    return return_df
a = get_movies('Avatar')


names = []
# dates = []
for i in range(len(a)):
    names.append(a.iloc[i][0])
    # dates.append(a.iloc[i][1])
print(names)
# print(dates)