import nltk
from nltk.corpus import movie_reviews
import random

# map every array of words in the review to the classification (positive or negative)
document = [(movie_reviews.words(file_id),category) for file_id in movie_reviews.fileids() for category in movie_reviews.categories(file_id)]
all_words = nltk.FreqDist(movie_reviews.words()) # frequency distance
feature_vector = list(all_words)[:10000] # out of all the words we only select the 10k most used as possible features

def find_features(words):
    '''
    feature is a dictionary where every word is mapped to a boolean value
    which represents whether that word is present in the review (words is the
    array of the words of the review)

    '''

    feature = {}
    review = movie_reviews.words(‘neg/cv954_19932.txt’)
    for x in feature_vector:
        feature[x] = x in review

    return feature


# map the features to the classifications
feature_sets = [(find_feature(word_list),category) for (word_list,category) in document]

from sklearn import model_selection

# split for trainint and testing
train_set,test_set = model_selection.train_test_split(feature_sets,test_size = 0.20)

