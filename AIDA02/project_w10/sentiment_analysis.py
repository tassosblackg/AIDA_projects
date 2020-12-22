# Week 10 ML&NLP
# Sentiment Analysis on IMDB dataset
# Classification using Naive Bayes

import nltk
# nltk.download('movie_reviews') # run only the first time
# nltk.download('stopwords')    # run only the first time
from nltk.corpus import movie_reviews as mr
from nltk.corpus import stopwords
from nltk import FreqDist as FD
import string
from random import shuffle


# clean words, i.e. remove stopwords and punctuation
def clean_words(words, stopwords_english):
    words_clean = []
    for word in words:
        word = word.lower()
        if word not in stopwords_english and word not in string.punctuation:
            words_clean.append(word)
    return words_clean

# feature extractor function for unigram
def bag_of_words(words):
    words_dictionary = dict([word, True] for word in words)
    return words_dictionary

# feature extractor function for ngrams (bigram)
def bag_of_ngrams(words, n=2):
    words_ng = []
    for item in iter(nltk.ngrams(words, n)):
        words_ng.append(item)
    words_dictionary = dict([word, True] for word in words_ng)
    return words_dictionary

#----------------------------------------------------------------------------
#               Data/Corpus Info
#----------------------------------------------------------------------------
# Print some statistics about movie_reviews corpus
print(type(mr))

# Files' names
# print(mr.fileids())

print (len(mr.fileids()))
# num of  positive reviews
print ('\nPositive reviews = ',len(mr.fileids('pos')))

# num of negative reviews
print ('\nNegative reviews = ',len(mr.fileids('neg')))

#----------------------------------------------------------------------------
#               Word Tokenize by category
#----------------------------------------------------------------------------
pos_reviews = []
for fileid in mr.fileids('pos'):
    words = mr.words(fileid)
    pos_reviews.append(words)

neg_reviews = []
for fileid in mr.fileids('neg'):
    words = mr.words(fileid)
    neg_reviews.append(words)

# 20 first positive/negative reviews' words
print (pos_reviews[0][:20])
print (neg_reviews[0][:20])

#----------------------------------------------------------------------------
#               Preprocess Remove Stopwords and punctuation
#----------------------------------------------------------------------------
# Get the stopwords for english language
stopwords_english = stopwords.words('english')
print('\nStopWords_en = \n',stopwords)

# ----------- | Testing using bag of unigrams |------------------------------
# positive_reviews unique words
# pos_reviews_set = []
# for words in pos_reviews:
#     words_clean = clean_words(words, stopwords_english)
#     pos_reviews_set.append((bag_of_words(words_clean), 'pos'))
#
# # negative_reviews unique words
# neg_reviews_set = []
# for words in neg_reviews:
#     words_clean= clean_words(words, stopwords_english)
#     neg_reviews_set.append((bag_of_words(words_clean), 'neg'))

# print ('\n',pos_reviews_set[0])

# -------------- |Testing method using ngrams with n=2|---------
important_words = ['above', 'below', 'off', 'over', 'under', 'more', 'most', 'such', 'no', 'nor', 'not', 'only', 'so', 'than', 'too', 'very', 'just', 'but']

stopwords_english_for_bigrams = set(stopwords_english) - set(important_words)

pos_reviews_set = []
for words in pos_reviews:
    words_clean = clean_words(words, stopwords_english_for_bigrams)
    pos_reviews_set.append((bag_of_ngrams(words_clean), 'pos'))

# negative_reviews unique words
neg_reviews_set = []
for words in neg_reviews:
    words_clean= clean_words(words, stopwords_english_for_bigrams)
    neg_reviews_set.append((bag_of_ngrams(words_clean), 'neg'))

# ------ Random Shuffle data -------------------------

shuffle(pos_reviews_set)
shuffle(neg_reviews_set)

#  ------- Get same amound of data from both categories and Split
# 20% for test 80% for train first 200 from each category for test set
test_set = pos_reviews_set[:200] + neg_reviews_set[:200]
train_set = pos_reviews_set[200:] + neg_reviews_set[200:]

print('\n Test_set size= ',len(test_set),'\nTrain_set size= ',len(train_set))

#----------------------------------------------------------------------------
#              Classification Task
#----------------------------------------------------------------------------
classifier = nltk.NaiveBayesClassifier.train(train_set)

accuracy = nltk.classify.accuracy(classifier, test_set)
print('\n Test set accuracy= ',accuracy)

print ('\n Most informative fetures/words=',classifier.show_most_informative_features(15))
