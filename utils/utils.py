import json
import operator
import random

print("Loading tracks and playlists..")
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Tracks.json", encoding="utf8") as f:
    TRACKS = json.load(f)
#Maybe we can get a smaller version of this file because we only really need a couple playlists
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Playlists.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)
print('Tracks and playlists loaded!')


def get_top_x_random_popular_uris():
    tracks_dict = {}
    tracks_list = list(TRACKS.keys())
    for i in range(len(TRACKS)):
        uri = tracks_list[i]
        tracks_dict.update({uri: 0})

    for i in range(len(PLAYLISTS)):
        if uri == 'spotify:track:6RQ97mq9F7QFRecMxmmdxS':
            break
        playlist = PLAYLISTS[i]['tracks']
        for uri in playlist:
            if uri == 'spotify:track:6RQ97mq9F7QFRecMxmmdxS':
                break
            tracks_dict.update({uri: tracks_dict[uri] + 1})

    tracks_dict = sorted(tracks_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_uris = []
    for i in range (len(tracks_dict)):
        sorted_uris.append(tracks_dict[i][0])
    sample = random.sample(range(1, 100), 10)
    chosen_uris = []
    for i in range(len(sample)):
        chosen_uris.append(sorted_uris[sample[i]])
    return chosen_uris

