__author__ = 'jason'
from textblob.classifiers import NaiveBayesClassifier
from __future__ import division
# ^- so that 3/2 returns 1.5 and not 1


class NewsAggregator:
    def __init__(self, similarity_threshold):
        self.articles = dict()      # key: article id, value: NewsArticle instance
        self.topics = dict()        # key: topic id , value: list of article ids
        self.classifiers = dict()   # key: classified variable (string), value: NaiveBayesClassifier
        self.next_topic_id = 1
        self.similarity_threshold = similarity_threshold    # value from 0 to 1 that defines the least percentage
                                                            # of similarity needed for two articles to be on the same
                                                            # topic.

    def add_article(self, article):
        # call classify_article() to see if it matches another one
        # if not, update the classifier with the data of that article and add it to topics

        self.articles[article.id] = article     # store article for future reference

        if len(self.topics) == 0:               # if there are no topics (empty DB)
            self.add_topic(article)             # create new one based on the article
        else:
            topic_id = self.classify_article(article)
            if topic_id == -1:                  # no match was found
                self.add_topic(article)         # then create new topic
            else:                               # matching topic found
                self.topics[topic_id].append(article.id)    # add article to topic's list
                # if we need to update classifiers, do it here
                #
                #

    def add_topic(self, article):
        # create a new topic based on the article
        # put the article id on the list of the topic
        # and add it's attributes to the classifiers as a new class

        self.topics[self.next_topic_id] = [article.id]
        self.next_topic_id += 1

        # create classifiers for each variable of the article and add them to the
        # classifiers dictionary of the NewsAggregator

    def classify_article(self, article):
        # classify the article with the classifier(s)
        # return the id of the matching topic if any, else return -1

        l_classifiers_results = []
        for classified_var in self.classifiers:
            l_classifiers_results.append(1)

        total = sum(l_classifiers_results)
        matching_score = total/len(l_classifiers_results)

        if matching_score >= self.similarity_threshold:

    def foo(self, article, classified_var):
        classifier = self.classifiers[classified_var]
