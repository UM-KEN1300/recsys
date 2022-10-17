import json
import pandas as pd
from lenskit.algorithms import Recommender
from lenskit.algorithms.item_knn import ItemItem
from explanations import explanations

tracksIndex = 4
import time
#Collaborative filtering approach after the dataset has been preprocessed
start_time = time.time()
print("Creating Ratings Dataframe...")
with open("/data/Playlists_small.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)
df_playlists = pd.read_json('../data/Playlists.json')
ratings_df = pd.read_csv('../data/ratings.csv')
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
print("--- %s seconds ---" % (time.time() - start_time))

#Print out results
selected_user = 0
selected_tracks_useruser = recsys.recommend(selected_user, num_recs)
#Print the names of the recommended songs
print(df_playlists.iloc[0]['name'])
print(selected_tracks_useruser)

#Print out explanation for each chosen song
for i in range(len(selected_tracks_useruser)):
    explanations.explanation_individual(selected_tracks_useruser.loc[i, 'item'], PLAYLISTS[0]['tracks'])



