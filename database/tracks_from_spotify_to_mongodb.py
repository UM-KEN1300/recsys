from pymongo import MongoClient
from os import listdir
from os.path import isfile, join
import json

MONGO = MongoClient('localhost', 27017)

DB_PLAYLISTS = MONGO['Spotify']['Playlists']
DB_TRACKS = MONGO['Spotify']['Tracks']

# Define Spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
## Create Spotipy client, and authenticate only once. We can continue using this client with the token we already received.
SPOTIFY = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials('5afff963a0eb4740a9d011b7f334adb0','59b20833720548fe8149542b00223130'))


res = SPOTIFY.audio_features('spotify:track:0UaMYEvWZi0ZqiDOoHU3YI')[0]
DATA_PATH = "../dataset/data/"

data_slices = [f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f))]

for file in data_slices:
    print("Parsing file", file)
    full_path = join(DATA_PATH, file)
    f = open(full_path)
    data = json.load(f)

    for playlist in data['playlists']:
        tracks = [t for t in playlist['tracks']]
        track_uris = [t['track_uri'] for t in playlist['tracks']]
        for track in tracks:
            track_uri = track['track_uri']
            track_in_db = DB_TRACKS.find_one({"track_uri": track_uri})
            if track_in_db is None:
                print("Track", track_uri, " does not exists in db!!!")
                res = SPOTIFY.audio_features(track_uri)[0]
                current_record = {
                "track_name": track["track_name"],
                "track_uri": res["uri"],
                "album_uri": track["album_uri"],
                "artist_uri": track["artist_uri"],
                "danceability": res["danceability"],
                "energy": res["energy"],
                "key": res["key"],
                "loudness": res["loudness"],
                "mode": res["mode"],
                "speechiness": res["speechiness"],
                "acousticness": res["acousticness"],
                "instrumentalness": res["instrumentalness"],
                "liveness": res["liveness"],
                "valence": res["valence"],
                "tempo": res["tempo"],
                'duration_ms': res["duration_ms"],
                'time_signature': res["time_signature"]
                }
                DB_TRACKS.insert_one(current_record)
            else:
                print("Track", track_uri, "already exists in db.")
    # Closing file
    f.close()