import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import Recommenders
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
import difflib
import time





# start = time.time()
# popular = get_popular_music()
# popular_songs = []

# for n in range(10):
#     popular_songs.append(popular.iloc[n][0])
# end = time.time()

# print(popular_songs, "\n", (end-start))


# def music_content_recommender(slice1, slice2):
#     music = pd.read_csv('./millions_set/newsong_data.csv')

#     # resample the data to 5000 rows since dataset is too large
#     music = music.loc[slice1:slice2]
#     music = music.drop('url', axis=1).reset_index(drop=True)

#     # music = music.sample(n=5000).drop('url', axis=1).reset_index(drop=True)

#     features = ['genres', 'artist_name']

#     for feature in features:
#         music[feature] = music[feature].fillna('')

#     def create_soup(x):
#         try:
#             return x['genres'] + " " + x['artist_name']
#         except:
#             print("Error occured creating soup")

#     music['soup'] = music.apply(create_soup, axis=1)

#     tfidf = TfidfVectorizer(analyzer='word', stop_words='english')
#     print('-----------------')
#     count_matrix = tfidf.fit_transform(music['soup'])

#     # cos_similar = cosine_similarity(count_matrix)
#     cos_similar = linear_kernel(count_matrix, count_matrix)
#     cos_similar.shape

#     similarities = {}

#     for i in range(len(cos_similar)):
#         # Now we'll sort each element in cosine_similarities and get the indexes of the songs.
#         similar_indices = cos_similar[i].argsort()[:-50:-1]
#         # After that, we'll store in similarities each name of the 50 most similar songs.

#         similarities[music['title'].iloc[i]] = [
#             (cos_similar[i][x], music['title'][x], music['artist_name'][x]) for x in similar_indices][:]

#     return similarities


# class ContentBasedRecommender:
#     def __init__(self, matrix):
#         self.matrix_similar = matrix

#     def _print_message(self, song, recom_song):
#         rec_items = len(recom_song)

#         print(f'The {rec_items} recommended songs for {song} are:')
#         for i in range(rec_items):
#             print(f"Number {i+1}:")
#             print(
#                 f"{recom_song[i][1]} by {recom_song[i][2]} with {round(recom_song[i][0], 3)} similarity score")
#             print("--------------------")

#     def recommend(self, song):
#         # Get song to find recommendations for
#         song = song
#         # Get number of songs to recommend
#         # number_songs = number
#         # Get the number of songs most similars from matrix similarities
#         recom_song = self.matrix_similar[song][:]
#         # print each item
#         # self._print_message(song=song, recom_song=recom_song)
#         return recom_song


# start = time.time()
# similarities = music_content_recommender(0, (0 + 5000))

# recommendations = ContentBasedRecommender(similarities)

# results = recommendations.recommend('Silent Night')

# hold_results = list()

# for each in range(len(results)):
#     hold_results.append(results[each][1])

# end = time.time()

# print(hold_results, "\n", (end - start))
