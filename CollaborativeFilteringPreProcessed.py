import json
import pandas as pd
import lenskit as lk
from lenskit.algorithms import Recommender
from lenskit.algorithms.item_knn import ItemItem
from groups import explanations
tracksIndex = 4
import time

start_time = time.time()
print("Creating Ratings Dataframe...")
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Playlists_small.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)
df_playlists = pd.read_json('data/Playlists.json')
ratings_df = pd.read_csv('data/ratings.csv')
ratings_df.columns=['user', 'item']
df_tracks = pd.read_json('data/tracks.json')
print("Playlists Ratings created!")
print("--- %s seconds ---" % (time.time() - start_time))

#Basically copied from lab
num_recs = 10
k = 15
item_item = ItemItem(k, min_nbrs=3, center=False, feedback='implicit', use_ratings=False)
recsys = Recommender.adapt(item_item)
start_time = time.time()
recsys.fit(ratings_df)
print("--- %s seconds ---" % (time.time() - start_time))


selected_user = 0
selected_tracks_useruser = recsys.recommend(selected_user, num_recs)
#Print the names of the recommended songs
print(df_playlists.iloc[0]['name'])
print(selected_tracks_useruser)

for i in range(len(selected_tracks_useruser)):
    explanations.explanation_individual(selected_tracks_useruser.loc[i, 'item'], PLAYLISTS[0]['tracks'])



