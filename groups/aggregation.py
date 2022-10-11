import json
import math
import compute_ratings

print("Loading tracks and playlists..")
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Tracks.json", encoding="utf8") as f:
    TRACKS = json.load(f)
#Maybe we can get a smaller version of this file cause we only really need a couple playlists
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Playlists_small.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)
print('Tracks and playlists loaded!')

playlist_1 = PLAYLISTS[0]['tracks']
print("Playlist 1, " + PLAYLISTS[0]['name'] + " added, with " + str(len(playlist_1)) + " songs.")
playlist_2 = PLAYLISTS[1]['tracks']
print("Playlist 2, " + PLAYLISTS[1]['name'] + " added, with " + str(len(playlist_2)) + " songs.")
playlist_3 = PLAYLISTS[2]['tracks']
print("Playlist 3, " + PLAYLISTS[2]['name'] + " added, with " + str(len(playlist_3)) + " songs.")
playlist_4 = PLAYLISTS[3]['tracks']
print("Playlist 4, " + PLAYLISTS[3]['name'] + " added, with " + str(len(playlist_4)) + " songs.")

tracks = playlist_1 + playlist_2 + playlist_3 + playlist_4


target_size = math.floor((len(playlist_1) + len(playlist_2) + len(playlist_3) + len(playlist_4))/4)
print("Target playlist will contain " + str(target_size) + " songs.")


ratings_playlist_1, ratings_playlist_2, ratings_playlist_3, ratings_playlist_4 = compute_ratings.compute_ratings(playlist_1, playlist_2, playlist_3, playlist_4)
print(ratings_playlist_1)



