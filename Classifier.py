__author__ = 'jason'
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import Utils

class Classifier:

    def __init__(self, content_type, initial_content):
        self.content_type = content_type    # a string with that describes the type of data to be stored
        self.content = initial_content

    # This function compute the similarity of the object stored with the given content
    # if the two objects are of the same type a normalized score [0.1] is returned
    # else the return value is -1
    def classify(self, content_type, content):
        if self.content_type != content_type:   # contents do not match
            return -1                           # error

        score = 0
        if content_type == "hashtags":
            score = Utils.list_similarity(self.content, content)
        elif



