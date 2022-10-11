import json
from similarity import cosine_similarity
print("Loading tracks and playlists..")
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Tracks.json", encoding="utf8") as f:
    TRACKS = json.load(f)
#Maybe we can get a smaller version of this file cause we only really need a couple playlists
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Playlists_small.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)
print('Tracks and playlists loaded!')

def add_own_songs(playlist, ratings):
    for i in range(len(playlist)):
        ratings.update({playlist[i]: 1})
def compute_ratings(playlist_1, playlist_2, playlist_3, playlist_4):
    playlists = [playlist_1, playlist_2, playlist_3, playlist_4]
    other_ratings_playlist_1 = {}
    other_ratings_playlist_2 = {}
    other_ratings_playlist_3 = {}
    other_ratings_playlist_4 = {}

    add_own_songs(playlist_1, other_ratings_playlist_1)
    add_own_songs(playlist_2, other_ratings_playlist_2)
    add_own_songs(playlist_3, other_ratings_playlist_3)
    add_own_songs(playlist_4, other_ratings_playlist_4)
    for i in range(1, 4):
        playlist = playlists[i]
        for j in range(len(playlist)):
            similarity_sum = 0
            for k in range(len(playlist_1)):
                similarity_sum += cosine_similarity.cosine_similarity_by_uri(playlist_1[k], playlist[j])
            other_ratings_playlist_1.update({playlist[j]: (similarity_sum / len(playlist_1))})

    for i in range(0, 4):
        if i != 1:
            playlist = playlists[i]
            for j in range(len(playlist)):
                similarity_sum = 0
                for k in range(len(playlist_2)):
                    similarity_sum += cosine_similarity.cosine_similarity_by_uri(playlist_2[k], playlist[j])
                other_ratings_playlist_2.update({playlist[j]: (similarity_sum / len(playlist_2))})

    for i in range(0, 4):
        if i != 2:
            playlist = playlists[i]
            for j in range(len(playlist)):
                similarity_sum = 0
                for k in range(len(playlist_3)):
                    similarity_sum += cosine_similarity.cosine_similarity_by_uri(playlist_3[k], playlist[j])
                other_ratings_playlist_3.update({playlist[j]: (similarity_sum / len(playlist_3))})

    for i in range(0, 3):
        if i != 2:
            playlist = playlists[i]
            for j in range(len(playlist)):
                similarity_sum = 0
                for k in range(len(playlist_4)):
                    similarity_sum += cosine_similarity.cosine_similarity_by_uri(playlist_4[k], playlist[j])
                other_ratings_playlist_4.update({playlist[j]: (similarity_sum / len(playlist_4))})



    return other_ratings_playlist_1, other_ratings_playlist_2, other_ratings_playlist_3, other_ratings_playlist_4