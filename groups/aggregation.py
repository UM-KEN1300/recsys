import json
import math
import compute_ratings
import operator

from groups import explanations

print("Loading tracks and playlists..")
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Tracks.json", encoding="utf8") as f:
    TRACKS = json.load(f)
# Maybe we can get a smaller version of this file cause we only really need a couple playlists
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Playlists_small.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)
print('Tracks and playlists loaded!')

playlist_1 = PLAYLISTS[0]['tracks']
print("Playlist 1, " + PLAYLISTS[0]['name'] +
      " added, with " + str(len(playlist_1)) + " songs.")
playlist_2 = PLAYLISTS[1]['tracks']
print("Playlist 2, " + PLAYLISTS[1]['name'] +
      " added, with " + str(len(playlist_2)) + " songs.")
playlist_3 = PLAYLISTS[2]['tracks']
print("Playlist 3, " + PLAYLISTS[2]['name'] +
      " added, with " + str(len(playlist_3)) + " songs.")
playlist_4 = PLAYLISTS[3]['tracks']
print("Playlist 4, " + PLAYLISTS[3]['name'] +
      " added, with " + str(len(playlist_4)) + " songs.")
tracks = playlist_1 + playlist_2 + playlist_3 + playlist_4

target_size = 50
print("Target playlist will contain " + str(target_size) + " songs.")

ratings_playlist_1, ratings_playlist_2, ratings_playlist_3, ratings_playlist_4 = compute_ratings.compute_ratings(
    playlist_1, playlist_2, playlist_3, playlist_4)

print("AVERAGE: ")
# AVERAGE GROUP RATING
ratings_AVG = {}
for i in range(len(tracks)):
    uri = tracks[i]
    rating_user_1 = ratings_playlist_1[uri]
    rating_user_2 = ratings_playlist_2[uri]
    rating_user_3 = ratings_playlist_3[uri]
    rating_user_4 = ratings_playlist_4[uri]
    final_rating = (rating_user_1+rating_user_2+rating_user_3+rating_user_4)/4
    ratings_AVG.update({uri: final_rating})
ratings_AVG = sorted(ratings_AVG.items(),
                     key=operator.itemgetter(1), reverse=True)

final_playlist_AVG = []
for i in range(target_size):
    print("Song " + str(i+1) + ": " + TRACKS[ratings_AVG[i][0]]
          ['track_name'] + " with a rating of " + str(ratings_AVG[i][1]) + ".")
    final_playlist_AVG.append(ratings_AVG[i][0])


for song in final_playlist_AVG:
    user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
    min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song],
                     ratings_playlist_3[song], ratings_playlist_4[song])
    user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[
        song] else 2 if min_rating == ratings_playlist_2[song] else 3 if min_rating == ratings_playlist_3[song] else 4
    explanations.explanation_groups_AVG(
        playlist_1, final_playlist_AVG, song, user_that_likes_song, user_that_dislikes_song)

for song in playlist_1:
    user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
    min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song],
                     ratings_playlist_3[song], ratings_playlist_4[song])
    user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[song] else 2 if min_rating == ratings_playlist_2[
        song] else 3 if min_rating == ratings_playlist_3[song] else 4 if min_rating == ratings_playlist_4[song] else 0
    explanations.explanation_groups_AVG(
        playlist_1, final_playlist_AVG, song, user_that_likes_song, user_that_dislikes_song)

# LEAST MISERY
ratings_LEAST_MISERY = {}
for i in range(len(tracks)):
    uri = tracks[i]
    rating_user_1 = ratings_playlist_1[uri]
    rating_user_2 = ratings_playlist_2[uri]
    rating_user_3 = ratings_playlist_3[uri]
    rating_user_4 = ratings_playlist_4[uri]
    final_rating = min([rating_user_1, rating_user_2,
                       rating_user_3, rating_user_4])
    ratings_LEAST_MISERY.update({uri: final_rating})
ratings_LEAST_MISERY = sorted(
    ratings_LEAST_MISERY.items(), key=operator.itemgetter(1), reverse=True)

final_playlist_LEAST_MISERY = []
for i in range(target_size):
    print("Song " + str(i+1) + ": " + TRACKS[ratings_LEAST_MISERY[i][0]]
          ['track_name'] + " with a rating of " + str(ratings_LEAST_MISERY[i][1]) + ".")
    final_playlist_LEAST_MISERY.append(ratings_LEAST_MISERY[i][0])


for song in final_playlist_LEAST_MISERY:
    user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
    min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song],
                     ratings_playlist_3[song], ratings_playlist_4[song])
    user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[
        song] else 2 if min_rating == ratings_playlist_2[song] else 3 if min_rating == ratings_playlist_3[song] else 4
    explanations.explanation_groups_LM(
        playlist_1, final_playlist_LEAST_MISERY, song, user_that_likes_song, user_that_dislikes_song)

for song in playlist_1:
    user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
    min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song],
                     ratings_playlist_3[song], ratings_playlist_4[song])
    user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[song] else 2 if min_rating == ratings_playlist_2[
        song] else 3 if min_rating == ratings_playlist_3[song] else 4 if min_rating == ratings_playlist_4[song] else 0
    explanations.explanation_groups_LM(
        playlist_1, final_playlist_LEAST_MISERY, song, user_that_likes_song, user_that_dislikes_song)

# LEAST MISERY + MOST PLEASURE + WITHOUT MISERY
ratings_LM_MP_WM = {}
for i in range(len(tracks)):
    uri = tracks[i]
    rating_user_1 = ratings_playlist_1[uri]
    rating_user_2 = ratings_playlist_2[uri]
    rating_user_3 = ratings_playlist_3[uri]
    rating_user_4 = ratings_playlist_4[uri]
    if rating_user_1 & rating_user_2 & rating_user_3 & rating_user_4 >= 0.45:
        final_rating = min(rating_user_1, rating_user_2, rating_user_3, rating_user_4) + \
            max(rating_user_1, rating_user_2, rating_user_3, rating_user_4)
        ratings_LM_MP_WM.update({uri: final_rating})
    else:
        continue
ratings_LM_MP_WM = sorted(ratings_LM_MP_WM.items(),
                          key=operator.itemgetter(1), reverse=True)

final_playlist_LM_MP_WM = []
for i in range(target_size):
    print("Song " + str(i+1) + ": " + TRACKS[ratings_LM_MP_WM[i][0]]
          ['track_name'] + " with a rating of " + str(ratings_LM_MP_WM[i][1]) + ".")
    final_playlist_LM_MP_WM.append(ratings_LM_MP_WM[i][0])


for song in final_playlist_LM_MP_WM:
    user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
    min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song],
                     ratings_playlist_3[song], ratings_playlist_4[song])
    user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[
        song] else 2 if min_rating == ratings_playlist_2[song] else 3 if min_rating == ratings_playlist_3[song] else 4
    explanations.explanation_groups_LM_MP_WM(
        playlist_1, final_playlist_LM_MP_WM, song, user_that_likes_song, user_that_dislikes_song)

for song in playlist_1:
    user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
    min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song],
                     ratings_playlist_3[song], ratings_playlist_4[song])
    user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[song] else 2 if min_rating == ratings_playlist_2[
        song] else 3 if min_rating == ratings_playlist_3[song] else 4 if min_rating == ratings_playlist_4[song] else 0
    explanations.explanation_groups_LM_MP_WM(
        playlist_1, final_playlist_LM_MP_WM, song, user_that_likes_song, user_that_dislikes_song)
