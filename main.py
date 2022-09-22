# shows track info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import json
import spotipy.util as util
from pprint import pprint



# load json into python gets a dict: data[‘playlists’][i] gives the i’th playlist as a dict again
#
# then data[‘playlists’][i][tracks] gives a list of the tracks through which we can access the track_uri and artist_uri among others
#
# artist_uri gives a list of genres which I assume is important for the RS itself



with open('dataset/data/mpd.slice.0-999.json', 'r') as f:
    data = json.load(f)

track_uris = []

for track in data['playlists'][0]['tracks']:
    track_uris.append(track['track_uri'])
track_info_collection = []

artist_uris = []

for track in data['playlists'][0]['tracks']:
    artist_uris.append(track['artist_uri'])
artist_info_collection = []

for urn in track_uris:
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials('e2c8b67438464676b834d0ea4b5d1a62','7a6a551c670644928dcead3ea5279ed4'))
    track = sp.track(urn)
    track_info_collection.append(track)

for urn in artist_uris:
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials('e2c8b67438464676b834d0ea4b5d1a62','7a6a551c670644928dcead3ea5279ed4'))
    artist = sp.artist(urn)
    artist_info_collection.append(artist)
print(track_info_collection[0])
print(artist_info_collection[0])

