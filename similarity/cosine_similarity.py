import json
from numpy import dot
from numpy.linalg import norm

with open("D:/Users/Dino/Recommender Systems/Project/recsys/data/Tracks.json", encoding="utf8") as f:
    TRACKS = json.load(f)

#Gets certain features that might be relevant for similarity
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


def cosine_similarity(list_1, list_2):
    list_1 = get_relevant_features(list_1)
    list_2 = get_relevant_features(list_2)
    cos_sim = dot(list_1, list_2) / (norm(list_1) * norm(list_2))
    return cos_sim

def get_track_by_index(index):
    return list(list(TRACKS.values())[index].values())


def cosine_similarity_by_uri(uri_1, uri_2):
    list_1 = list(TRACKS[uri_1].values())
    list_2 = list(TRACKS[uri_2].values())
    return cosine_similarity(list_1, list_2)


