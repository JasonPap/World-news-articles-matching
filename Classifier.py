__author__ = 'jason'

import Utils


class Classifier:
    def __init__(self, content_type, initial_content):
        self.content_type = content_type  # a string with that describes the type of data to be stored
        self.content = initial_content

    # This function compute the similarity of the object stored with the given content
    # if the two objects are of the same type a normalized score [0.1] is returned
    # else the return value is -1
    def classify(self, content_type, content):
        if self.content_type != content_type:  # contents do not match
            return -1  # error

        score = 0
        if content_type == "hashtags":
            score = Utils.list_similarity(self.content, content)
        elif content_type == "persons":
            score = Utils.list_similarity(self.content, content)
        elif content_type == "organizations":
            score = Utils.list_similarity(self.content, content)
        elif content_type == "locations":
            score = Utils.list_similarity(self.content, content)
        elif content_type == "countries":
            score = Utils.list_similarity(self.content, content)
        elif content_type == "places":
            score = Utils.list_similarity(self.content, content)
        elif content_type == "noun_phrases":
            np_str1 = ' '.join(self.content)
            np_str2 = ' '.join(content)  # convert a list of strings to a single string
            score = Utils.text_similarity(np_str1, np_str2)
        elif content_type == "plaintext":
            score = Utils.text_similarity(self.content, content)
        elif content_type == "title":
            score = Utils.text_similarity(self.content, content)
        elif content_type == "description":
            score = Utils.text_similarity(self.content, content)

        return score

    # Update the content of the classifier
    def update(self, content):
        self.content = content
