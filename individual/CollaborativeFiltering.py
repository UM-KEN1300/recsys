import json
import pandas as pd
from lenskit.algorithms import Recommender
from lenskit.algorithms.item_knn import ItemItem
from explanations import explanations
import numpy as np
from utils import utils
from similarity import cosine_similarity

tracksIndex = 4
import time
#Collaborative filtering approach after the dataset has been preprocessed
start_time = time.time()
print("Creating Ratings Dataframe...")
with open("/data/Playlists_small.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)
df_playlists = pd.read_json('../data/Playlists_small.json')
ratings_df = pd.read_csv('../data/ratings.csv')
ratings_new_df = pd.read_csv('../data/ratings_new.csv')
ratings_df.columns=['user', 'item']
df_tracks = pd.read_json('../data/Tracks.json')
print("Playlists Ratings created!")
print("--- %s seconds ---" % (time.time() - start_time))

#Lenskit CF approach
num_recs = 10
k = 15
item_item = ItemItem(k, min_nbrs=3, center=False, feedback='implicit', use_ratings=False)
recsys = Recommender.adapt(item_item)
start_time = time.time()
recsys.fit(ratings_df)
similarity_sum_baseline = 0
similarity_sum_recommendations = 0
print("--- %s seconds ---" % (time.time() - start_time))
for i in range(100):
    #Print out results
    selected_user = i
    selected_tracks_useruser = recsys.recommend(selected_user, num_recs)
    #Print the names of the recommended songs
    # print(df_playlists.iloc[i]['name'])
    # print(selected_tracks_useruser)
    actual_recommendations = []
    #Print out explanation for each chosen song
    for j in range(len(selected_tracks_useruser)):
        # explanations.explanation_individual(selected_tracks_useruser.loc[j, 'item'], PLAYLISTS[i]['tracks'])
        actual_recommendations.append(selected_tracks_useruser.loc[j, 'item'])
    baseline_recommendations = utils.get_top_x_random_popular_uris()
    playlist = PLAYLISTS[i]
    baseline_similarity = cosine_similarity.compute_playlist_list_similarity(playlist, baseline_recommendations)
    print("Baseline similarity: " + str(baseline_similarity))
    similarity_sum_baseline += baseline_similarity
    recommendation_similarity = cosine_similarity.compute_playlist_list_similarity(playlist, actual_recommendations)
    print("Recommendation similarity: " + str(recommendation_similarity))
    similarity_sum_recommendations += recommendation_similarity

print("Baseline: "+ str(similarity_sum_baseline/100))
print("Recommendation: "+ str(similarity_sum_recommendations/100))

def similarity_evaluation(i, actual_recommendations):
    baseline_recommendations = utils.get_top_x_random_popular_uris()
    playlist = PLAYLISTS[i]
    baseline_similarity = cosine_similarity.compute_playlist_list_similarity(playlist, baseline_recommendations)
    print("Baseline similarity: " + str(baseline_similarity))
    recommendation_similarity = cosine_similarity.compute_playlist_list_similarity(playlist, actual_recommendations)
    print("Recommendation similarity: " + str(cosine_similarity.compute_playlist_list_similarity(playlist, actual_recommendations)))

