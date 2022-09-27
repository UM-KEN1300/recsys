import json
import pandas as pd
tracksIndex = 4
#Create a dataframe from the json file - these work with LensKit and are generally very useful
print("Creating Playlists Dataframe...")
df_playlists = pd.read_json('data/PlaylistsTest.json')
print("Playlists Dataframe created!")

print("Creating Tracks Dataframe...")
df_tracks = pd.read_json('data/TracksTest.json')
print("Tracks Dataframe created")


#We can access playlist j by calling df_playlists[j], and then the Tracks list that belongs to the playlist is at [j][tracksIndex]
#The line below prints a list of tracks, which belongs to playlist 0
print(df_playlists.iloc[0][tracksIndex])
#So here we get the first track on the first playlist
track = df_playlists.iloc[0][tracksIndex][0]

#Then we can access the track content through df_tracks (which acts like a dictionary, track is the uri here)
track_info = df_tracks[track]
print(track_info)




