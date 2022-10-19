import json
from similarity import compute_ratings
import operator
import random
from explanations import explanations
import numpy as np
print("Loading tracks and playlists..")
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Tracks.json", encoding="utf8") as f:
    TRACKS = json.load(f)
#Maybe we can get a smaller version of this file because we only really need a couple playlists
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Playlists_small.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)
print('Tracks and playlists loaded!')


#Load in any 4 playlist to base recommendations on
def aggregate(indices):
    index_1, index_2, index_3, index_4 = indices
    playlist_1 = PLAYLISTS[index_1]['tracks']
    print("Playlist 1, " + PLAYLISTS[0]['name'] + " added, with " + str(len(playlist_1)) + " songs.")
    playlist_2 = PLAYLISTS[index_2]['tracks']
    print("Playlist 2, " + PLAYLISTS[1]['name'] + " added, with " + str(len(playlist_2)) + " songs.")
    playlist_3 = PLAYLISTS[index_3]['tracks']
    print("Playlist 3, " + PLAYLISTS[2]['name'] + " added, with " + str(len(playlist_3)) + " songs.")
    playlist_4 = PLAYLISTS[index_4]['tracks']
    print("Playlist 4, " + PLAYLISTS[3]['name'] + " added, with " + str(len(playlist_4)) + " songs.")
    tracks = playlist_1 + playlist_2 + playlist_3 + playlist_4
    playlist_list = [playlist_1, playlist_2, playlist_3, playlist_4]
    indices = [index_1,index_2,index_3,index_4]
    index = 0
    for playlist in playlist_list:
        print("playlist " + str(indices[index]) + "////////////////////////////////////////////////////")
        for song in playlist:
            print(TRACKS[song]['track_name'])
        index+=1
    #Size of the final playlist
    target_size = 30
    print("Target playlist will contain " + str(target_size) + " songs.")

    #Compute all estimated ratings of songs that are not in the initial playlist based on cosine similarity of certain features fetched from the spotify API
    ratings_playlist_1, ratings_playlist_2, ratings_playlist_3, ratings_playlist_4 = compute_ratings.compute_ratings(playlist_1, playlist_2, playlist_3, playlist_4)


    print("AVERAGE: ")
    #AVERAGE GROUP RATING aggregation approach
    ratings_AVG = {}
    for i in range(len(tracks)):
        uri = tracks[i]
        rating_user_1 = ratings_playlist_1[uri]
        rating_user_2 = ratings_playlist_2[uri]
        rating_user_3 = ratings_playlist_3[uri]
        rating_user_4 = ratings_playlist_4[uri]
        final_rating = (rating_user_1+rating_user_2+rating_user_3+rating_user_4)/4
        ratings_AVG.update({uri:final_rating})
    ratings_AVG = sorted(ratings_AVG.items(), key=operator.itemgetter(1), reverse=True)

    final_playlist_AVG = []
    for i in range(target_size):
        print("Song " + str(i+1) + ": " + TRACKS[ratings_AVG[i][0]]['track_name'] + " with a rating of " + str(ratings_AVG[i][1]) + ".")
        final_playlist_AVG.append(ratings_AVG[i][0])

    #Print explanations for all songs that are in the final playlist but not in the user's playlist
    for song in final_playlist_AVG:
        user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
        min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song], ratings_playlist_3[song], ratings_playlist_4[song])
        user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[song] else 2 if min_rating == ratings_playlist_2[song] else 3 if min_rating == ratings_playlist_3[song] else 4
        explanations.explanation_groups_AVG(playlist_1, final_playlist_AVG, song, user_that_likes_song, user_that_dislikes_song)

    #Print explanations for all songs that are not in the final playlist but are in the user's playlist
    for song in playlist_1:
        user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
        min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song], ratings_playlist_3[song], ratings_playlist_4[song])
        user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[song] else 2 if min_rating == ratings_playlist_2[song] else 3 if min_rating == ratings_playlist_3[song] else 4 if min_rating == ratings_playlist_4[song] else 0
        explanations.explanation_groups_AVG(playlist_1, final_playlist_AVG, song, user_that_likes_song, user_that_dislikes_song)

    # LEAST MISERY + MOST PLEASURE + WITHOUT MISERY
    ratings_LM_MP_WM = {}
    threshold = 0.75
    for i in range(len(tracks)):
        uri = tracks[i]
        rating_user_1 = ratings_playlist_1[uri]
        rating_user_2 = ratings_playlist_2[uri]
        rating_user_3 = ratings_playlist_3[uri]
        rating_user_4 = ratings_playlist_4[uri]
        if rating_user_1 >= threshold and rating_user_2 >= threshold and rating_user_3 >= threshold and rating_user_4 >= threshold:
            final_rating = (min(rating_user_1, rating_user_2, rating_user_3, rating_user_4) +
                            max(rating_user_1, rating_user_2, rating_user_3, rating_user_4)) / 2
            ratings_LM_MP_WM.update({uri: final_rating})
        else:
            continue
    ratings_LM_MP_WM = sorted(ratings_LM_MP_WM.items(),
                              key=operator.itemgetter(1), reverse=True)

    final_playlist_LM_MP_WM = []
    for i in range(target_size):
        print("Song " + str(i + 1) + ": " + TRACKS[ratings_LM_MP_WM[i][0]]
        ['track_name'] + " with a rating of " + str(ratings_LM_MP_WM[i][1]) + ".")
        final_playlist_LM_MP_WM.append(ratings_LM_MP_WM[i][0])

    for song in final_playlist_LM_MP_WM:
        user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
        min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song],
                         ratings_playlist_3[song], ratings_playlist_4[song])
        user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[
            song] else 2 if min_rating == ratings_playlist_2[song] else 3 if min_rating == ratings_playlist_3[
            song] else 4
        # explanations.explanation_groups_LM_MP_WM(
        #     playlist_1, final_playlist_LM_MP_WM, song, user_that_likes_song, user_that_dislikes_song)

    for song in playlist_1:
        user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
        min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song],
                         ratings_playlist_3[song], ratings_playlist_4[song])
        user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[song] else 2 if min_rating == \
                                                                                        ratings_playlist_2[
                                                                                            song] else 3 if min_rating == \
                                                                                                            ratings_playlist_3[
                                                                                                                song] else 4 if min_rating == \
                                                                                                                                ratings_playlist_4[
                                                                                                                                    song] else 0
        # explanations.explanation_groups_LM_MP_WM(playlist_1, final_playlist_LM_MP_WM, song, user_that_likes_song, user_that_dislikes_song)

    print("LEAST MISERY: ")
    #LEAST MISERY aggregation approach
    ratings_LEAST_MISERY = {}
    for i in range(len(tracks)):
        uri = tracks[i]
        rating_user_1 = ratings_playlist_1[uri]
        rating_user_2 = ratings_playlist_2[uri]
        rating_user_3 = ratings_playlist_3[uri]
        rating_user_4 = ratings_playlist_4[uri]
        final_rating = min([rating_user_1, rating_user_2, rating_user_3, rating_user_4])
        ratings_LEAST_MISERY.update({uri:final_rating})
    ratings_LEAST_MISERY = sorted(ratings_LEAST_MISERY.items(), key=operator.itemgetter(1), reverse=True)

    final_playlist_LEAST_MISERY = []
    for i in range(target_size):
        print("Song " + str(i+1) + ": " + TRACKS[ratings_LEAST_MISERY[i][0]]['track_name'] + " with a rating of " + str(ratings_LEAST_MISERY[i][1]) + ".")
        final_playlist_LEAST_MISERY.append(ratings_LEAST_MISERY[i][0])

    #Print explanations for all songs that are in the final playlist but not in the user's playlist
    for song in final_playlist_LEAST_MISERY:
        user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
        min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song], ratings_playlist_3[song], ratings_playlist_4[song])
        user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[song] else 2 if min_rating == ratings_playlist_2[song] else 3 if min_rating == ratings_playlist_3[song] else 4
        explanations.explanation_groups_LM(playlist_1, final_playlist_LEAST_MISERY, song, user_that_likes_song, user_that_dislikes_song)

    #Print explanations for all songs that are not in the final playlist but are in the user's playlist
    for song in playlist_1:
        user_that_likes_song = 1 if song in playlist_1 else 2 if song in playlist_2 else 3 if song in playlist_3 else 4
        min_rating = min(ratings_playlist_1[song], ratings_playlist_2[song], ratings_playlist_3[song], ratings_playlist_4[song])
        user_that_dislikes_song = 1 if min_rating == ratings_playlist_1[song] else 2 if min_rating == ratings_playlist_2[song] else 3 if min_rating == ratings_playlist_3[song] else 4 if min_rating == ratings_playlist_4[song] else 0
        explanations.explanation_groups_LM(playlist_1, final_playlist_LEAST_MISERY, song, user_that_likes_song, user_that_dislikes_song)

    songs_in_playlist_1 = 0
    songs_in_playlist_2 = 0
    songs_in_playlist_3 = 0
    songs_in_playlist_4 = 0
    for song in final_playlist_AVG:
        if song in playlist_1:
            songs_in_playlist_1+=1
        if song in playlist_2:
            songs_in_playlist_2+=1
        if song in playlist_3:
            songs_in_playlist_3+=1
        if song in playlist_4:
            songs_in_playlist_4+=1

    print("AVERAGE:")
    print("Songs in final playlist from playlist 1: " + str(songs_in_playlist_1) + " from original " + str(len(playlist_1)))
    print("Songs in final playlist from playlist 2: " + str(songs_in_playlist_2) + " from original " + str(len(playlist_2)))
    print("Songs in final playlist from playlist 3: " + str(songs_in_playlist_3) + " from original " + str(len(playlist_3)))
    print("Songs in final playlist from playlist 4: " + str(songs_in_playlist_4) + " from original " + str(len(playlist_4)))

    print("Average similarity of chosen songs for user 1: ")
    similarity_user_1_sum = 0
    similarity_user_2_sum = 0
    similarity_user_3_sum = 0
    similarity_user_4_sum = 0
    for song in final_playlist_AVG:
        similarity_user_1_sum += ratings_playlist_1[song]
        similarity_user_2_sum += ratings_playlist_2[song]
        similarity_user_3_sum += ratings_playlist_3[song]
        similarity_user_4_sum += ratings_playlist_4[song]
    print("Average expected rating user 1: " + str(similarity_user_1_sum/target_size))
    print("Average expected rating user 2: " + str(similarity_user_2_sum/target_size))
    print("Average expected rating user 3: " + str(similarity_user_3_sum/target_size))
    print("Average expected rating user 4: " + str(similarity_user_4_sum/target_size))

    list_nums_AVG = [songs_in_playlist_1, songs_in_playlist_2, songs_in_playlist_3, songs_in_playlist_4]
    list_ratings_AVG = [similarity_user_1_sum/target_size,similarity_user_2_sum/target_size,similarity_user_3_sum/target_size,similarity_user_4_sum/target_size]
    print("LEAST MISERY:")
    songs_in_playlist_1 = 0
    songs_in_playlist_2 = 0
    songs_in_playlist_3 = 0
    songs_in_playlist_4 = 0
    for song in final_playlist_LEAST_MISERY:
        if song in playlist_1:
            songs_in_playlist_1+=1
        if song in playlist_2:
            songs_in_playlist_2+=1
        if song in playlist_3:
            songs_in_playlist_3+=1
        if song in playlist_4:
            songs_in_playlist_4+=1


    print("Songs in final playlist from playlist 1: " + str(songs_in_playlist_1) + " from original " + str(len(playlist_1)))
    print("Songs in final playlist from playlist 2: " + str(songs_in_playlist_2) + " from original " + str(len(playlist_2)))
    print("Songs in final playlist from playlist 3: " + str(songs_in_playlist_3) + " from original " + str(len(playlist_3)))
    print("Songs in final playlist from playlist 4: " + str(songs_in_playlist_4) + " from original " + str(len(playlist_4)))
    print("Average similarity of chosen songs for user 1: ")

    similarity_user_1_sum = 0
    similarity_user_2_sum = 0
    similarity_user_3_sum = 0
    similarity_user_4_sum = 0
    for song in final_playlist_LEAST_MISERY:
        similarity_user_1_sum += ratings_playlist_1[song]
        similarity_user_2_sum += ratings_playlist_2[song]
        similarity_user_3_sum += ratings_playlist_3[song]
        similarity_user_4_sum += ratings_playlist_4[song]

    print("Average expected rating user 1: " + str(similarity_user_1_sum/target_size))
    print("Average expected rating user 2: " + str(similarity_user_2_sum/target_size))
    print("Average expected rating user 3: " + str(similarity_user_3_sum/target_size))
    print("Average expected rating user 4: " + str(similarity_user_4_sum/target_size))
    list_nums_LM = [songs_in_playlist_1, songs_in_playlist_2, songs_in_playlist_3, songs_in_playlist_4]
    list_ratings_LM = [similarity_user_1_sum/target_size,similarity_user_2_sum/target_size,similarity_user_3_sum/target_size,similarity_user_4_sum/target_size]

    print("LM_MP_WM:")
    songs_in_playlist_1 = 0
    songs_in_playlist_2 = 0
    songs_in_playlist_3 = 0
    songs_in_playlist_4 = 0
    for song in final_playlist_LM_MP_WM:
        if song in playlist_1:
            songs_in_playlist_1 += 1
        if song in playlist_2:
            songs_in_playlist_2 += 1
        if song in playlist_3:
            songs_in_playlist_3 += 1
        if song in playlist_4:
            songs_in_playlist_4 += 1

    print("Songs in final playlist from playlist 1: " + str(songs_in_playlist_1) + " from original " + str(
        len(playlist_1)))
    print("Songs in final playlist from playlist 2: " + str(songs_in_playlist_2) + " from original " + str(
        len(playlist_2)))
    print("Songs in final playlist from playlist 3: " + str(songs_in_playlist_3) + " from original " + str(
        len(playlist_3)))
    print("Songs in final playlist from playlist 4: " + str(songs_in_playlist_4) + " from original " + str(
        len(playlist_4)))
    print("Average similarity of chosen songs for user 1: ")

    similarity_user_1_sum = 0
    similarity_user_2_sum = 0
    similarity_user_3_sum = 0
    similarity_user_4_sum = 0
    for song in final_playlist_LM_MP_WM:
        similarity_user_1_sum += ratings_playlist_1[song]
        similarity_user_2_sum += ratings_playlist_2[song]
        similarity_user_3_sum += ratings_playlist_3[song]
        similarity_user_4_sum += ratings_playlist_4[song]

    print("Average expected rating user 1: " + str(similarity_user_1_sum / target_size))
    print("Average expected rating user 2: " + str(similarity_user_2_sum / target_size))
    print("Average expected rating user 3: " + str(similarity_user_3_sum / target_size))
    print("Average expected rating user 4: " + str(similarity_user_4_sum / target_size))
    list_nums_LM_MP_WM = [songs_in_playlist_1, songs_in_playlist_2, songs_in_playlist_3, songs_in_playlist_4]
    list_ratings_LM_MP_WM = [similarity_user_1_sum / target_size, similarity_user_2_sum / target_size,
                       similarity_user_3_sum / target_size, similarity_user_4_sum / target_size]
    return list_nums_AVG, list_ratings_AVG, list_nums_LM, list_ratings_LM, list_nums_LM_MP_WM, list_ratings_LM_MP_WM


sum_list_nums_AVG = [0,0,0,0]
sum_list_ratings_AVG = [0,0,0,0]
sum_list_nums_LM = [0,0,0,0]
sum_list_ratings_LM = [0,0,0,0]
sum_list_nums_LM_MP_WM = [0,0,0,0]
sum_list_ratings_LM_MP_WM = [0,0,0,0]

num_samples = 10
for i in range(num_samples):
    indices = [1,2,12,14]#random.sample(range(0, len(PLAYLISTS)), 4)
    list_nums_AVG, list_ratings_AVG, list_nums_LM, list_ratings_LM, list_nums_LM_MP_WM, list_ratings_LM_MP_WM = aggregate(indices)

    sum_list_nums_AVG = np.add(sum_list_nums_AVG, list_nums_AVG)
    sum_list_ratings_AVG = np.add(sum_list_ratings_AVG, list_ratings_AVG)
    sum_list_nums_LM = np.add(sum_list_nums_LM, list_nums_LM)
    sum_list_ratings_LM = np.add(sum_list_ratings_LM, list_ratings_LM)
    sum_list_nums_LM_MP_WM = np.add(sum_list_nums_LM_MP_WM, list_nums_LM_MP_WM)
    sum_list_ratings_LM_MP_WM = np.add(sum_list_ratings_LM_MP_WM, list_ratings_LM_MP_WM)

sum_list_nums_AVG = np.divide(sum_list_nums_AVG, num_samples)
sum_list_ratings_AVG = np.divide(sum_list_ratings_AVG, num_samples)
sum_list_nums_LM = np.divide(sum_list_nums_LM, num_samples)
sum_list_ratings_LM = np.divide(sum_list_ratings_LM, num_samples)
sum_list_nums_LM_MP_WM = np.divide(sum_list_nums_LM_MP_WM, num_samples)
sum_list_ratings_LM_MP_WM = np.divide(sum_list_ratings_LM_MP_WM, num_samples)

print("AVERAGE:")
print("Average number of songs per list:")
print(sum_list_nums_AVG)
print("Average rating of songs per list:")
print(sum_list_ratings_AVG)
print("LEAST MISERY:")
print("Average number of songs per list: ")
print(sum_list_nums_LM)
print("Average rating of songs per list")
print(sum_list_ratings_LM)
print("LM_MP_WM:")
print("Average number of songs per list:")
print(sum_list_nums_LM_MP_WM)
print("Average rating of songs per list:")
print(sum_list_ratings_LM_MP_WM)

print("AVERAGE vs LEAST MISERY vs LM_MP_WM: ")
print(np.sum(sum_list_ratings_AVG))
print(np.sum(sum_list_ratings_LM))
print(np.sum(sum_list_ratings_LM_MP_WM))