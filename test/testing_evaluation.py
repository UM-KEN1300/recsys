import json
import pandas as pd
from lenskit.algorithms import Recommender
from lenskit.algorithms.basic import Fallback
from lenskit.algorithms.bias import Bias
from lenskit.algorithms.item_knn import ItemItem
from sklearn.model_selection import train_test_split
#from sklearn.metrics import precision_recall_fscore_support
from explanations import explanations
import numpy as np
from utils import utils
from similarity import cosine_similarity

ratings_new_df = pd.read_csv('../data/ratings_new.csv')
print("Playlists Ratings created!")

def merge_train(i, df_sliced_X, df_sliced_Y):
    train_X = pd.DataFrame()
    train_Y = pd.DataFrame()
    for j in range(len(df_sliced_X)):
        if j!=i:
            train_X = pd.concat([train_X, df_sliced_X[j]])
            train_Y = pd.concat([train_Y, df_sliced_Y[j]])
    return train_X, train_Y

def training_and_testing():
    ratings_new_df.columns = ['user', 'item', 'rating']
    # X = ratings_new_df[['user', 'item']]
    # Y = ratings_new_df[['rating']]
    #
    # df_sliced_X = np.array_split(X, 10)
    # df_sliced_Y = np.array_split(Y, 10)
    #
    # for i in range(len(df_sliced_X)):
    #     item_item = ItemItem(15, min_nbrs=3, center=False, feedback='implicit')
    #     base = Bias(damping=5)
    #     algo = Fallback(item_item, base)
    #     recsys = Recommender.adapt(algo)
    #     test_X, test_Y = df_sliced_X[i], df_sliced_Y[i]
    #     train_X, train_Y = merge_train(i, df_sliced_X, df_sliced_Y)
    #     recsys.fit(pd.concat([train_X, train_Y], axis=1))
    #
    #     test_X['predicted_rating'] = recsys.predict(pd.concat([test_X, test_Y], axis=1))
    #     print(test_X)


    train_df, test_df = train_test_split(ratings_new_df, test_size=0.2)
    item_item = ItemItem(15, min_nbrs=3, center=False, feedback='implicit')
    recsys = Recommender.adapt(item_item)
    recsys.fit(train_df)

    test_df['predicted_rating'] = recsys.predict(test_df)
    print(test_df.to_string())






training_and_testing()
