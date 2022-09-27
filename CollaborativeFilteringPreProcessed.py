import json
import pandas as pd
import lenskit as lk
from lenskit.algorithms import Recommender
from lenskit.algorithms.item_knn import ItemItem
tracksIndex = 4
import time

start_time = time.time()
print("Creating Ratings Dataframe...")
ratings_df = pd.read_csv('data/ratings.csv')
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

#Todo: what is a user? It would make sense it is the same type as in the ratings_df DF (id in this case) but that doesnt seem to work


for u in range(3):
    selected_user = u
    selected_tracks_useruser = recsys.recommend(selected_user, num_recs)
    #Print the names of the recommended songs
    print(selected_tracks_useruser)
    for i in range(len(selected_tracks_useruser)):
        print(df_tracks[selected_tracks_useruser.loc[i, 'item']]['track_name'])


