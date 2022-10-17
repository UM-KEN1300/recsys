from pymongo import MongoClient
from os import listdir
from os.path import isfile, join
import json

MONGO = MongoClient('localhost', 27017)

DB_PLAYLISTS = MONGO['Spotify']['Playlists']

DATA_PATH = "../dataset/data/"
data_slices = [f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f))]

for file in data_slices:
    full_path = join(DATA_PATH, file)
    f = open(full_path)
    data = json.load(f)

    for playlist in data['playlists']:
        current_record = {
            "name": playlist['name'],
            "collaborative": eval(playlist['collaborative'].title()),
            "num_albums": playlist['num_albums'],
            "num_followers": playlist['num_followers'],
            "tracks": [t['track_uri'] for t in playlist['tracks']]
        }
        print(current_record)
        rec = DB_PLAYLISTS.insert_one(current_record)
    # Closing file
    f.close()

# inserting the data in the database
#rec = DB_PLAYLISTS.insert_one(rec)