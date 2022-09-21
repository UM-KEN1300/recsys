# shows track info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import spotipy.util as util
from pprint import pprint


if len(sys.argv) > 1:
    urn = sys.argv[1]
else:
    urn = 'spotify:track:0Svkvt5I79wficMFgaqEQJ'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials('e2c8b67438464676b834d0ea4b5d1a62','7a6a551c670644928dcead3ea5279ed4'))

track = sp.track(urn)
pprint(track)
