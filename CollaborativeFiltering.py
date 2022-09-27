import json
import pandas as pd
import lenskit as lk
from lenskit.algorithms import Recommender
from lenskit.algorithms.item_knn import ItemItem
tracksIndex = 4

#Note that I created test version files which are very short just to see if things run
print("Creating Playlists Dataframe...")
df_playlists = pd.read_json('data/PlaylistsTest.json')
print("Playlists Dataframe created!")
print("Creating Tracks Dataframe...")
df_tracks = pd.read_json('data/TracksTest.json')
print("Tracks Dataframe created")

#Create empty dataframe with needed columns
ratings_df = pd.DataFrame(columns=['user', 'item'])


#Unsure about this - how else can we reference user?
id = 0
#Go over all the playlists
for i in range(len(df_playlists)):
    #Locate them (enhanced for loops with dataframes are messy)
    playlist = df_playlists.iloc[i]
    #For each playlist see go over all tracks
    for j in range(len(playlist[tracksIndex])):
        #Add a row to ratings_df with the playlist id and the track uri
        track = playlist[tracksIndex][j]
        new_entry = pd.DataFrame({'user':id, 'item':track}, index=[0])
        ratings_df = pd.concat([ratings_df, new_entry])
    id+=1

#Basically copied from lab
num_recs = 10
k = 15
item_item = ItemItem(k, min_nbrs=3, center=False, feedback='implicit', use_ratings=False)
recsys = Recommender.adapt(item_item)
recsys.fit(ratings_df)

#Todo: what is a user? It would make sense it is the same type as in the ratings_df DF (id in this case) but that doesnt seem to work
selected_user = 0
selected_tracks_useruser = recsys.recommend(selected_user, num_recs)
#Print the names of the recommended songs
for i in range(len(selected_tracks_useruser)):
    print(df_tracks[selected_tracks_useruser[i]['track_name']])