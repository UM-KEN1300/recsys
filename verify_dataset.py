from pymongo import MongoClient
from os import listdir
from os.path import isfile, join
import json

MONGO = MongoClient('localhost', 27017)

DB_PLAYLISTS = MONGO['Spotify']['Playlists']
DB_TRACKS = MONGO['Spotify']['Tracks']

playlist_docs = DB_PLAYLISTS.find({})
problematic_tracks = []
for doc in playlist_docs:
    tracks = doc["tracks"]
    
    for track in tracks:
        track_in_tracks = DB_TRACKS.find_one({"track_uri": track})
        if track_in_tracks is None:
            print("theres a problem with track", track)
            problematic_tracks += track

print("done!")
print(problematic_tracks)
        