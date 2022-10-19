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




import json
import pandas as pd
from lenskit.algorithms import Recommender
from lenskit.algorithms.basic import Fallback
from lenskit.algorithms.bias import Bias
from lenskit.algorithms.item_knn import ItemItem
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
import numpy as np


ratings_new_df = pd.read_csv('data/ratings_new.csv')
print("Playlists Ratings created!")


def merge_train(i, df_sliced_X, df_sliced_Y):
    train_X = pd.DataFrame()
    train_Y = pd.DataFrame()
    for j in range(len(df_sliced_X)):
        if j!=i:
            train_X = pd.concat([train_X, df_sliced_X[j]])
            train_Y = pd.concat([train_Y, df_sliced_Y[j]])
    return train_X, train_Y


def training_and_testing_original_dataset():
    ratings_new_df.columns = ['user', 'item', 'rating']

    X = ratings_new_df[['user', 'item']]
    Y = ratings_new_df[['rating']]

    df_sliced_X = np.array_split(X, 10)
    df_sliced_Y = np.array_split(Y, 10)

    total_accuracy = 0
    total_mean_predicted_rating = 0
    total_median_predicted_rating = 0
    total_standard_deviation_predicted_rating = 0
    lowest_value = 1
    highest_value = 0
    threshold = 0.11

    for i in range(len(df_sliced_X)):
         item_item = ItemItem(15, min_nbrs=3, center=False, feedback='implicit')
         base = Bias(damping=5)
         algo = Fallback(item_item, base)
         recsys = Recommender.adapt(algo)
         test_X, test_Y = df_sliced_X[i], df_sliced_Y[i]
         train_X, train_Y = merge_train(i, df_sliced_X, df_sliced_Y)
         recsys.fit(pd.concat([train_X, train_Y], axis=1))

         test = pd.concat([test_X, test_Y], axis=1)
         test['predicted_rating'] = recsys.predict(test)

         total_mean_predicted_rating += test['predicted_rating'].mean()
         total_median_predicted_rating += test['predicted_rating'].median()
         total_standard_deviation_predicted_rating += test['predicted_rating'].std()

         current_lowest = test['predicted_rating'].min()
         current_highest = test['predicted_rating'].max()
         print(current_lowest)
         print(current_highest)

         if current_highest > highest_value and current_highest <= 1:
             highest_value = current_highest

         if current_lowest < lowest_value and current_lowest >= 0:
             lowest_value = current_lowest

         test['predicted_relevant'] = test['predicted_rating'].apply(lambda x: 1 if x > threshold else 0)
         y_test = list(test['rating'])
         y_pred = list(test['predicted_relevant'])
         accuracy = balanced_accuracy_score(y_test, y_pred)
         total_accuracy += accuracy

    print("Lowest Value:\t" + str(lowest_value))
    print("Highest Value:\t" + str(highest_value))
    print("Mean:\t" + str(total_mean_predicted_rating / 10))
    print("Median:\t" + str(total_median_predicted_rating / 10))
    print("Standard Deviation:\t" + str(total_standard_deviation_predicted_rating / 10))
    print("Threshold used:\t" + str(threshold))
    print("Accuracy:\t" + str(total_accuracy/10))



def training_and_testing_sampled_dataset():
    ratings_new_df.columns = ['user', 'item', 'rating']
    positive_df = ratings_new_df.loc[(ratings_new_df['rating'] == 1)].copy()  # 6008 entries
    negative_df = ratings_new_df.loc[(ratings_new_df['rating'] == 0)].copy()  # 516 091 entries --> So entire 'ratings_new_df' heavily sparse.

    ratings_df = pd.concat([positive_df.sample(n=4000), negative_df.sample(n=4000)], axis=0)
    shuffled_ratings_df = ratings_df.sample(frac=1)

    X = shuffled_ratings_df[['user', 'item']]
    Y = shuffled_ratings_df[['rating']]

    df_sliced_X = np.array_split(X, 10)
    df_sliced_Y = np.array_split(Y, 10)

    total_accuracy = 0
    total_mean_predicted_rating = 0
    total_median_predicted_rating = 0
    total_standard_deviation_predicted_rating = 0
    lowest_value = 1
    highest_value = 0
    threshold = 0.5

    for i in range(len(df_sliced_X)):
         item_item = ItemItem(15, min_nbrs=3, center=False, feedback='implicit')
         base = Bias(damping=5)
         algo = Fallback(item_item, base)
         recsys = Recommender.adapt(algo)
         #recsys = Recommender.adapt(item_item)
         test_X, test_Y = df_sliced_X[i], df_sliced_Y[i]
         train_X, train_Y = merge_train(i, df_sliced_X, df_sliced_Y)
         recsys.fit(pd.concat([train_X, train_Y], axis=1))

         test = pd.concat([test_X, test_Y], axis=1)
         test['predicted_rating'] = recsys.predict(test)
         print(test)

         total_mean_predicted_rating += test['predicted_rating'].mean()
         total_median_predicted_rating += test['predicted_rating'].median()
         total_standard_deviation_predicted_rating += test['predicted_rating'].std()

         current_lowest = test['predicted_rating'].min()
         current_highest = test['predicted_rating'].max()

         if current_highest > highest_value:
             highest_value = current_highest

         if current_lowest < lowest_value:
             lowest_value = current_lowest

         test['predicted_relevant'] = test['predicted_rating'].apply(lambda x: 1 if x > threshold else 0)
         y_test = list(test['rating'])
         y_pred = list(test['predicted_relevant'])
         accuracy = balanced_accuracy_score(y_test, y_pred)
         total_accuracy += accuracy

    print("Lowest Value:\t" + str(lowest_value))
    print("Highest Value:\t" + str(highest_value))
    print("Mean:\t" + str(total_mean_predicted_rating / 10))
    print("Median:\t" + str(total_median_predicted_rating / 10))
    print("Standard Deviation:\t" + str(total_standard_deviation_predicted_rating / 10))
    print("Threshold used:\t" + str(threshold))
    print("Accuracy:\t" + str(total_accuracy / 10))



