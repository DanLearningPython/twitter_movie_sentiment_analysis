import pickle
import re
import os

from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer


class Predict:

    def __init__(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.vectorizer = CountVectorizer(decode_error="replace", vocabulary=pickle.load(open(__location__+"/words.pkl", "rb")))
        self.classifier = joblib.load(__location__+'/movie_reviews.pkl')

    def classify(self, vectorized_tweets):
        # returns array of classifications. 0 = negative, 1 = positive
        # convert np array into python list
        return (self.classifier.predict(vectorized_tweets)).tolist()

    def transform(self, clean_tweets):
        # turns tweets into vector of words
        return self.vectorizer.transform(clean_tweets)

    def clean_tweets(self, reviews):
        # Remove HTML
        reviews_text = list(map(lambda x: BeautifulSoup(x, 'html.parser').get_text(), reviews))
        #
        # Remove non-letters
        reviews_text = list(map(lambda x: re.sub("[^a-zA-Z]"," ", x), reviews_text))
        #
        # Convert words to lower case and split them
        words = list(map(lambda x: x.lower().split(), reviews_text))
        #
        # Remove stop words
        set_of_stopwords = set(stopwords.words("english"))
        meaningful_words = list(map(lambda x: [w for w in x if not w in set_of_stopwords], words))

        clean_review = list(map(lambda x: ' '.join(x), meaningful_words))

        return clean_review

    def prepare(self, raw_tweets):
        # Takes in list of tweet strings

        try:
            #prepares tweet/s for classification
            cleaned_tweets = self.clean_tweets(raw_tweets)
            vectorized_tweets = self.transform(cleaned_tweets)
            tweet_array = vectorized_tweets.toarray()

            #array of tweet vectors
            return tweet_array
        except:
            return None
