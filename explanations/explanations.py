from similarity import compute_ratings
import json

with open("/data/Tracks.json", "r", encoding='utf-8') as rf:
    TRACKS = json.load(rf) #is a dictionary! containing tracks that exists through all playlists

#Explanation for a chosen song that is not in the users playlist
def explanation_groups_XYZ(playlist_explain, uri, user_that_likes_song):
    most_similar, second_most_similar = compute_ratings.compute_ratings_explanations(uri, playlist_explain)
    print(TRACKS[uri]['track_name'] + " is in the playlist because user " + str(user_that_likes_song) + " likes that song and it is similar to " + TRACKS[most_similar]['track_name'] + ' and ' + TRACKS[second_most_similar]['track_name'] + ' which you like.')

#Explanation #2 for a chosen song that is not in the users playlist
def explanation_groups_XY(playlist_explain, uri, user_that_likes_song):
    most_similar, second_most_similar = compute_ratings.compute_ratings_explanations(uri, playlist_explain)
    print(TRACKS[uri]['track_name'] + " is in the playlist because user " + str(user_that_likes_song) + " likes that song and it is similar to " + TRACKS[most_similar]['track_name'] + ' and ' + TRACKS[second_most_similar]['track_name'] + ' which you like.')

#Explanation for a song that is in the users playlist that is not chosen when using LM
def explanation_groups_missing_LM(uri, user_that_dislikes):
    print(TRACKS[uri]['track_name'] + " is not in the playlist because user " + str(user_that_dislikes) + " really hates that song.")

#Explanation for a song that is in the users playlist that is not chosen when using AVG
def explanation_groups_missing_AVG(uri, user_that_dislikes):
    print(TRACKS[uri]['track_name'] + " is not in the playlist because user " + str(user_that_dislikes) + " really hates that song.")


#Explanation for the collaborative filtering recommendation
def explanation_individual(uri, playlist):
    most_similar, second_most_similar = compute_ratings.compute_ratings_explanations(uri, playlist)
    print(TRACKS[uri]['track_name'] + " is recommended to you because it is similar to " + TRACKS[most_similar]['track_name'] + ' and ' + TRACKS[second_most_similar]['track_name'] + ' which are in your playlist.')

#Calls another method based on input
def explanation_groups_AVG(playlist_explain, final_playlist, uri, user_that_likes_song, user_that_dislikes):
    #If the song passed is in the user's playlist but not in the final playlist
    if uri in playlist_explain and uri not in final_playlist:
        explanation_groups_missing_AVG(uri, user_that_dislikes)
    #If the song passed is not in the user's playlist but is in the final playilst
    elif uri in final_playlist:
        explanation_groups_XYZ(playlist_explain, uri, user_that_likes_song)

#Calls another method based on input
def explanation_groups_LM(playlist_explain, final_playlist, uri, user_that_likes_song, user_that_dislikes):
    #If the song passed is in the user's playlist but not in the final playlist
    if uri in playlist_explain and uri not in final_playlist:
        explanation_groups_missing_LM(uri, user_that_dislikes)
    #If the song passed is not in the user's playlist but is in the final playilst
    elif uri in final_playlist:
        explanation_groups_XYZ(playlist_explain, uri, user_that_likes_song)