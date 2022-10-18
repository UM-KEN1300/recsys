from groups import compute_ratings
import json
from random import randint
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Tracks.json", "r", encoding='utf-8') as rf:
    # is a dictionary! containing tracks that exists through all playlists
    TRACKS = json.load(rf)


def explanation_groups_XYZ(playlist_explain, uri, user_that_likes_song):
    most_similar, second_most_similar = compute_ratings.compute_ratings_explanations(
        uri, playlist_explain)
    print(TRACKS[uri]['track_name'] + " is in the playlist because user " + str(user_that_likes_song) + " likes that song and it is similar to " +
          TRACKS[most_similar]['track_name'] + ' and ' + TRACKS[second_most_similar]['track_name'] + ' which you like.')


def explanation_groups_XY(playlist_explain, uri, user_that_likes_song):
    most_similar, second_most_similar = compute_ratings.compute_ratings_explanations(
        uri, playlist_explain)
    print(TRACKS[uri]['track_name'] + " is in the playlist because user " + str(user_that_likes_song) + " likes that song and it is similar to " +
          TRACKS[most_similar]['track_name'] + ' and ' + TRACKS[second_most_similar]['track_name'] + ' which you like.')


def explanation_groups_missing_LM(uri, user_that_dislikes):
    print(TRACKS[uri]['track_name'] + " is not in the playlist because user " +
          str(user_that_dislikes) + " really hates that song.")


def explanation_groups_missing_AVG(uri, user_that_dislikes):
    print(TRACKS[uri]['track_name'] + " is not in the playlist because user " +
          str(user_that_dislikes) + " really hates that song.")


def explanation_groups_missing_LM_MP_WM(uri, user_that_dislikes):
    print(TRACKS[uri]['track_name'] + " is not in the playlist because user " +
          str(user_that_dislikes) + " really hates that song.")


def explanation_individual(uri, playlist):
    most_similar, second_most_similar = compute_ratings.compute_ratings_explanations(
        uri, playlist)
    print(TRACKS[uri]['track_name'] + " is recommended to you because it is similar to " + TRACKS[most_similar]
          ['track_name'] + ' and ' + TRACKS[second_most_similar]['track_name'] + ' which are in your playlist.')


def explanation_groups_AVG(playlist_explain, final_playlist, uri, user_that_likes_song, user_that_dislikes):
    # If the song passed is in the user's playlist but not in the final playlist
    if uri in playlist_explain and uri not in final_playlist:
        explanation_groups_missing_AVG(uri, user_that_dislikes)
    # If the song passed is not in the user's playlist but is in the final playilst
    elif uri in final_playlist:
        explanation_groups_XYZ(playlist_explain, uri, user_that_likes_song)


def explanation_groups_LM(playlist_explain, final_playlist, uri, user_that_likes_song, user_that_dislikes):
    # If the song passed is in the user's playlist but not in the final playlist
    if uri in playlist_explain and uri not in final_playlist:
        explanation_groups_missing_LM(uri, user_that_dislikes)
    # If the song passed is not in the user's playlist but is in the final playilst
    elif uri in final_playlist:
        explanation_groups_XYZ(playlist_explain, uri, user_that_likes_song)


def explanation_groups_LM_MP_WM(playlist_explain, final_playlist, uri, user_that_likes_song, user_that_dislikes):
    # If the song passed is in the user's playlist but not in the final playlist
    if uri in playlist_explain and uri not in final_playlist:
        explanation_groups_missing_LM_MP_WM(uri, user_that_dislikes)
    # If the song passed is not in the user's playlist but is in the final playilst
    elif uri in final_playlist:
        explanation_groups_XYZ(playlist_explain, uri, user_that_likes_song)
