import json
import compute_ratings
from similarity import cosine_similarity
print("Loading tracks and playlists..")
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Tracks.json", encoding="utf8") as f:
    TRACKS = json.load(f)
#Maybe we can get a smaller version of this file cause we only really need a couple playlists
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Playlists_small.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)
print('Tracks and playlists loaded!')

playlist_1 = PLAYLISTS[0]['tracks']
playlist_2 = PLAYLISTS[1]['tracks']
playlist_3 = PLAYLISTS[2]['tracks']
playlist_4 = PLAYLISTS[3]['tracks']

other_ratings_playlist_1, other_ratings_playlist_2, other_ratings_playlist_3, other_ratings_playlist_4 = compute_ratings.compute_ratings(playlist_1, playlist_2, playlist_3, playlist_4)
print(other_ratings_playlist_1, other_ratings_playlist_2, other_ratings_playlist_3, other_ratings_playlist_4)