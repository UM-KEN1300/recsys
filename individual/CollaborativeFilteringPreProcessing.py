import json
import pandas as pd
import lenskit as lk
from lenskit.algorithms import Recommender
from lenskit.algorithms.item_knn import ItemItem
tracksIndex = 4
import time

#Note that I created test version files which are very short just to see if things run
start_time = time.time()
# print("Creating Playlists Dataframe...")
# df_playlists = pd.read_json('../data/Playlists_small.json')
# print("Playlists Dataframe created!")
# print("Creating Tracks Dataframe...")
# df_tracks = pd.read_json('../data/Tracks.json')

with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Tracks.json", encoding="utf8") as f:
    TRACKS = json.load(f)
#Maybe we can get a smaller version of this file because we only really need a couple playlists
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Playlists_very_small.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)
print("Tracks Dataframe created")
print("--- %s seconds ---" % (time.time() - start_time))
#Create empty dataframe with needed columns
ratings_df = pd.DataFrame(columns=['user', 'item'])

#Unsure about this - how else can we reference user?
id = 0
#Go over all the playlists

start_time = time.time()
# for i in range(10000):#len(df_playlists)):
#     #Locate them
#     playlist = df_playlists.iloc[i]
#     #For each playlist see go over all tracks
#     for j in range(len(playlist[tracksIndex])):
#         #Add a row to ratings_df with the playlist id and the track uri
#         track = playlist[tracksIndex][j]
#         new_entry = pd.DataFrame({'user':id, 'item':track}, index=[0])
#         #ratings_df = pd.concat([ratings_df, new_entry])
#         new_entry.to_csv('D:/Users/Dino/Recommender Systems/Project/recsys/data/ratings.csv', mode='a', index=False, encoding='utf-8', header=False)
#     id+=1


tracks_list = list(TRACKS.keys())
i=0
name = PLAYLISTS[i]['name']
num_albums = PLAYLISTS[i]['num_albums']
for i in range(len(PLAYLISTS)):
    print(i)
    j = 0
    track = tracks_list[j]
    name = PLAYLISTS[i]['name']
    num_albums = PLAYLISTS[i]['num_albums']
    playlist = PLAYLISTS[i]['tracks']
    while track!= "spotify:track:5XUVWIOICLzDB5scsFzqkh":
        track = tracks_list[j]
        if track in playlist:
            new_entry = pd.DataFrame({'user': i, 'item': track, 'rating':1}, index=[0])
        else:
            new_entry = pd.DataFrame({'user': i, 'item': track, 'rating':0}, index=[0])
        new_entry.to_csv('D:/Users/Dino/Recommender Systems/Project/recsys/data/ratings_new.csv', mode='a', index=False, encoding='utf-8', header=False)
        j+=1


print("--- %s seconds ---" % (time.time() - start_time))


# num_recs = 10
# k = 15
# item_item = ItemItem(k, min_nbrs=3, center=False, feedback='implicit', use_ratings=False)
# recsys = Recommender.adapt(item_item)
# start_time = time.time()
# recsys.fit(ratings_df)
# print("--- %s seconds ---" % (time.time() - start_time))
# selected_user = 0
# selected_tracks_useruser = recsys.recommend(selected_user, num_recs)
# #Print the names of the recommended songs
# print(selected_tracks_useruser)
# for i in range(len(selected_tracks_useruser)):
#     print(df_tracks[selected_tracks_useruser.loc[i, 'item']]['track_name'])