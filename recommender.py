import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel


df1 = pd.read_csv('./tmdb.csv')



df2 = df1['soup']

df2 = df2.fillna('')
count = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
count_matrix = count.fit_transform(df2)

cosine_sim2 = linear_kernel(count_matrix, count_matrix)
cosine_sim2.shape

df2 = df2.reset_index()

indices = pd.Series(df1.index, index=df1['title'])
all_titles = [df1['title'][i] for i in range(len(df1['title']))]

def index_from_title(title):
    title_list = df1['title'].tolist()


    common = difflib.get_close_matches(title, title_list, 1)

    titlesim = common[0]

    return  titlesim

def get_recommendations(title):
    title = index_from_title(title)
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df1['title'].iloc[movie_indices]
    dat = df1['release_date'].iloc[movie_indices]
    rating = df1['vote_average'].iloc[movie_indices]
    genre = df1['genres'].iloc[movie_indices]
    return_df = pd.DataFrame(columns=['Title','Year','rating','genre'])
    return_df['Title'] = tit
    return_df['Year'] = dat
    return_df['rating'] = rating
    return_df['genre'] = genre
    return return_df






