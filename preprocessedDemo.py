#This version of loading data directly reads the json content and dumps into memory.
#Just to load, you'll need an additional ~3GB RAM. It's just a nice conveince.
import json

#Load Data (Put JSON data into ./data/ folder!!!)
print("Loading playlists data...")
with open("./data/Playlists.json", "r", encoding='utf-8') as rf:
    PLAYLISTS = json.load(rf) #is a list containing all playlists
print("Loading tracks data...")    
with open("./data/Tracks.json", "r", encoding='utf-8') as rf:
    TRACKS = json.load(rf) #is a dictionary! containing tracks that exists through all playlists

print('Loaded', len(PLAYLISTS), 'playlists and', len(TRACKS), 'tracks.')

print("\n===== Getting a playlist =====\n")
first_playlist = PLAYLISTS[0] #To get a playlist, iterate through PLAYLISTS
print(first_playlist)

print("\n\n===== Getting a track from playlist =====\n")
tracks_in_first_playlist = first_playlist["tracks"] #is a list of track URI's that are in this playlist
random_track_uri = tracks_in_first_playlist[0] #is a track URI such as `spotify:track:6I9VzXrHxO9rA9A5euc8Ak`
print(random_track_uri)

print("\n\n===== Getting the tracks features =====\n")
# To get features of a track:
features_of_track = TRACKS[random_track_uri]
print(features_of_track) #track URI's are keys of the TRACKS dictionary.