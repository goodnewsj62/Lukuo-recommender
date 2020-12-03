import time
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel


# df1 = pd.read_csv('./tmdb.csv')


# df2 = df1['soup']

# df2 = df2.fillna('')
# count = TfidfVectorizer(analyzer='word', ngram_range=(
#     1, 2), min_df=0, stop_words='english')
# count_matrix = count.fit_transform(df2)

# # cosine_sim2 = linear_kernel(count_matrix, count_matrix)
# # cosine_sim2.shape

# df2 = df2.reset_index()

# indices = pd.Series(df1.index, index=df1['title'])
# # all_titles = [df1['title'][i] for i in range(len(df1['title']))]


# def index_from_title(title):
#     title_list = df1['title'].tolist()

#     common = difflib.get_close_matches(title, title_list, 1)

#     titlesim = common[0]

#     return titlesim


# def get_recommendations(title):
#     title = index_from_title(title)
#     cosine_sim = cosine_similarity(count_matrix, count_matrix)
#     idx = indices[title]
#     sim_scores = list(enumerate(cosine_sim[idx]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     sim_scores = sim_scores[:11]
#     movie_indices = [i[0] for i in sim_scores]
#     tit = df1['title'].iloc[movie_indices]
#     dat = df1['release_date'].iloc[movie_indices]
#     rating = df1['vote_average'].iloc[movie_indices]
#     genre = df1['genres'].iloc[movie_indices]
#     return_df = pd.DataFrame(columns=['Title', 'Year', 'rating', 'genre'])
#     return_df['Title'] = tit
#     return_df['Year'] = dat
#     return_df['rating'] = rating
#     return_df['genre'] = genre
#     return return_df


class Recommender:
    def __init__(self, recom_type, slice1=0, slice2=1, tv_data=None):
        self.type = recom_type
        self.tv_data = tv_data

        # cause recommender count from zero unlike db where id start from 1
        self.slice1 = slice1 - 1
        self.slice2 = slice2 - 1

    def dataframe_tv(self):
        df = pd.DataFrame({'title': [n.title for n in self.tv_data], 'soup': [
            n.soup for n in self.tv_data]})

        return df

    def create_soup(self, x):
        try:
            # return x['genres'] + " " + x['artist_name']+" "+x['title']
            return x['genres'] + " " + x['artist_name']
        except:
            print("Error occured creating soup")

    def recommender_engine(self):
        df1 = None
        df2 = None
        if self.type == 'movie':
            df1 = pd.read_csv('./tmdb.csv')
            df2 = df1['soup']
        elif self.type == 'music':
            df1 = pd.read_csv('./millions_set/newsong_data.csv')
            df1 = df1.loc[self.slice1:self.slice2]
            df1 = df1.drop('url', axis=1).reset_index(drop=True)
            # features = ['genres', 'artist_name', 'title']
            features = ['genres', 'artist_name']

            for feature in features:
                df1[feature] = df1[feature].fillna('')

            df1['soup'] = df1.apply(self.create_soup, axis=1)
            df2 = df1['soup']
        elif self.type == 'tv':
            df1 = self.dataframe_tv()
            df2 = df1['soup']

        df2 = df2.fillna('')

        count = TfidfVectorizer(analyzer='word', ngram_range=(
            1, 2), min_df=0, stop_words='english')
        count_matrix = count.fit_transform(df2)

        df2 = df2.reset_index()

        indices = pd.Series(df1.index, index=df1['title'])

        # print(df1)

        return df1, indices, count_matrix

    def index_from_title(self, title, df1):
        title_list = df1['title'].tolist()

        common = difflib.get_close_matches(title, title_list, 1)

        titlesim = common[0]

        return titlesim

    def get_recommendations(self, title):
        df1, indices, count_matrix = self.recommender_engine()
        title = self.index_from_title(title, df1)
        cosine_sim = cosine_similarity(count_matrix, count_matrix)

        idx = indices[title]
        sim_scores = None
        extra = []  # get extra index for multiple indeices index

        if self.type == "movie" or self.type == "tv":
            sim_scores = list(enumerate(cosine_sim[idx]))
        else:
            # usually we normally have multiple index so we only take that
            # of the first index
            try:
                sim_scores = list(enumerate(cosine_sim[idx[0]]))
                extra = extra + [(n + 1) for n in idx]
            except:
                sim_scores = list(enumerate(cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[:11]

        # special case for music where we have multiple music with the same name

        if extra:
            sim_scores = sim_scores[1:11]

        movie_indices = [i[0] for i in sim_scores]

        if self.type == "music":
            movie_indices = [i[0] + 1 for i in sim_scores]

        if self.type == "movie" or self.type == "tv":
            tit = df1['title'].iloc[movie_indices]
            return_df = pd.DataFrame(columns=['Title'])
            return_df['Title'] = tit
            return return_df

        if extra:
            movie_indices = extra + movie_indices

        return movie_indices


# start = time.time()
# recommend = Recommender('music', 1, (1+5000))
# # recommend = Recommender("movie")
# result_final = recommend.get_recommendations('Silent Night')
# # result_final = recommend.get_recommendations('hell boy')


# names = []

# for i in range(len(result_final)):
    # names.append(result_final.iloc[i][0])
#     names.append(result_final[i])

# end = time.time()

# print(names, "\n", (end - start))
