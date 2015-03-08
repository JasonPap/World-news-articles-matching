__author__ = 'jason'

from Classifier import *


class NewsAggregator:
    def __init__(self, similarity_threshold):
        self.articles = dict()      # key: article id, value: NewsArticle instance
        self.topics = dict()        # key: topic id , value: list of article ids
        self.classifiers = dict()   # key: classified variable (string), value: list of tuples (topic_id, classifier)
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
        topic_id = self.next_topic_id
        self.topics[topic_id] = [article.id]
        self.next_topic_id += 1

        # create classifiers for each variable of the article and add them to the
        # classifiers dictionary of the NewsAggregator
        for content_type in article.metadata:
            content = article.metadata[content_type]
            new_classifier = Classifier(content_type, content)
            if content_type in self.classifiers:
                self.classifiers[content_type].append((topic_id, new_classifier))
            else:
                self.classifiers[content_type] = [(topic_id, new_classifier)]

    def classify_article(self, article):
        # classify the article with the classifier(s)
        # return the id of the matching topic if any, else return -1

        l_classifiers_results = []
        for classified_var in self.classifiers:
            l_classifiers_results.append(1)

        total = sum(l_classifiers_results)
        matching_score = total/len(l_classifiers_results)

        # keep the highest of those greater than the similarity threshold
        if matching_score >= self.similarity_threshold:

    def foo(self, article, classified_var):
        classifier = self.classifiers[classified_var]
