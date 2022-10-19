import json
from similarity import cosine_similarity
print("Loading tracks and playlists..")
with open("../data/Tracks.json", encoding="utf8") as f:
    TRACKS = json.load(f)
#Maybe we can get a smaller version of this file cause we only really need a couple playlists
with open("../data/Playlists_small.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)
print('Tracks and playlists loaded!')

#Function to add all songs that are in the playlist to it's own rated songs with a value of 1
def add_own_songs(playlist, ratings):
    for i in range(len(playlist)):
        ratings.update({playlist[i]: 1})

#Method that estimates the ratings of other songs not in a playlist
def compute_ratings(playlist_1, playlist_2, playlist_3, playlist_4):
    #Create list of playlists and empty dictionaries for each playlist
    playlists = [playlist_1, playlist_2, playlist_3, playlist_4]
    other_ratings_playlist_1 = {}
    other_ratings_playlist_2 = {}
    other_ratings_playlist_3 = {}
    other_ratings_playlist_4 = {}

    #Add songs of each playlist to its rating
    add_own_songs(playlist_1, other_ratings_playlist_1)
    add_own_songs(playlist_2, other_ratings_playlist_2)
    add_own_songs(playlist_3, other_ratings_playlist_3)
    add_own_songs(playlist_4, other_ratings_playlist_4)


    #For all playlists except for the playlist we are looping over
    for i in range(1, 4):
        playlist = playlists[i]
        #Loop over the playlist
        for j in range(len(playlist)):
            similarity_sum = 0
            #And sum the similarities that song j has with each song k in the original playlist
            for k in range(len(playlist_1)):
                similarity_sum += cosine_similarity.cosine_similarity_by_uri(playlist_1[k], playlist[j])
            #Normalize the similarity and update
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
        playlist = playlists[i]
        for j in range(len(playlist)):
            similarity_sum = 0
            for k in range(len(playlist_4)):
                similarity_sum += cosine_similarity.cosine_similarity_by_uri(playlist_4[k], playlist[j])
            other_ratings_playlist_4.update({playlist[j]: (similarity_sum / len(playlist_4))})

    return other_ratings_playlist_1, other_ratings_playlist_2, other_ratings_playlist_3, other_ratings_playlist_4

#This method finds the two most similar songs in a playlist to a given URI
def compute_ratings_explanations(uri, playlist):
    highest_similarity = 0
    second_highest_similarity = 0
    most_similar = None
    second_most_similar = None
    for i in range(len(playlist)):
        if cosine_similarity.cosine_similarity_by_uri(uri, playlist[i])>second_highest_similarity:
            if cosine_similarity.cosine_similarity_by_uri(uri, playlist[i]) > highest_similarity:
                highest_similarity = cosine_similarity.cosine_similarity_by_uri(uri, playlist[i])
                second_most_similar = most_similar
                most_similar = playlist[i]
            else:
                second_most_similar = playlist[i]
                cosine_similarity.cosine_similarity_by_uri(uri, playlist[i])
    return most_similar, second_most_similar