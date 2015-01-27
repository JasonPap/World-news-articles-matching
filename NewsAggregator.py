__author__ = 'jason'
from textblob.classifiers import NaiveBayesClassifier


class NewsAggregator:
    def __init__(self):
        self.topics = dict()
        self.classifier = NaiveBayesClassifier()

    def add_article(self, article):
        # call classify_article() to see if it matches another one
        # if not, update the classifier with the data of that article and add it to topics
        if len(self.topics) == 0:
            self.add_topic(article)

        topic_id = self.classify_article(article)

    def add_topic(self, article):
        # create a new topic based on the article
        # and add it's attributes to the classifier as a new class


    def classify_article(self, article):
        # classify the article with the classifier(s)
        # return the id of the matching topic if any, else return -1