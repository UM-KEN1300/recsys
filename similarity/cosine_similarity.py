import json
from numpy import dot
from numpy.linalg import norm
from matplotlib import pyplot as plt
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Tracks.json", encoding="utf8") as f:
    TRACKS = json.load(f)
with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Playlists_small.json", encoding="utf8") as f:
    PLAYLISTS = json.load(f)

#Gets only relevant features: through experimenting and research found that these work best
def get_relevant_features(list):
    new_list = []
    new_list.append(list[0])
    new_list.append(list[1])
    new_list.append(list[5])
    new_list.append(list[6])
    new_list.append(list[7])
    new_list.append(list[8])
    new_list.append(list[9])
    return new_list

#Cosine similarity of two vectors/lists
def cosine_similarity(list_1, list_2):
    list_1 = get_relevant_features(list_1)
    list_2 = get_relevant_features(list_2)
    cos_sim = dot(list_1, list_2) / (norm(list_1) * norm(list_2))
    return cos_sim

#Utility method to access a track in a playlist by index
def get_track_by_index(index):
    return list(list(TRACKS.values())[index].values())

#Method to get cosine similarity directly through URI instead of having to access its features
def cosine_similarity_by_uri(uri_1, uri_2):
    list_1 = list(TRACKS[uri_1].values())
    list_2 = list(TRACKS[uri_2].values())
    return cosine_similarity(list_1, list_2)

def compute_intra_playlist_similarity():
    playlist_1 = PLAYLISTS[0]['tracks']
    total = 0
    print(playlist_1)

    similarities = []
    for playlist in PLAYLISTS:
        print(playlist)
        similarity = 0
        total = 0
        playlist_1 = playlist['tracks']
        for uri_1 in playlist_1:
            for uri_2 in playlist_1:
                if uri_1 != uri_2:
                    similarity += cosine_similarity_by_uri(uri_1, uri_2)
                    total += 1
        similarity = similarity / total
        similarities.append(similarity)

    fig, ax = plt.subplots(1, 1)
    plt.hist(similarities)
    ax.set_xlabel('similarity')
    ax.set_ylabel('# of playlists')
    plt.show()

def compute_playlist_similarity():
    similarities = []
    for playlist_1 in PLAYLISTS:
        playlist_1 = playlist_1['tracks']
        for playlist_2 in PLAYLISTS:
            playlist_2 = playlist_2['tracks']
            similarity = 0
            total = 0
            if playlist_1!=playlist_2:
                for uri_1 in playlist_1:
                    for uri_2 in playlist_2:
                        similarity += cosine_similarity_by_uri(uri_1, uri_2)
                        total += 1
                similarity = similarity / total
                similarities.append(similarity)

    fig, ax = plt.subplots(1, 1)
    plt.hist(similarities)
    ax.set_xlabel('similarity')
    ax.set_ylabel('# of playlists')
    plt.show()

compute_playlist_similarity()