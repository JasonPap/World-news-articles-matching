__author__ = 'jason'
from collections import Counter
import math


# main functions used by others
def list_similarity(list1, list2):
    c1, c2 = Counter(list1), Counter(list2)
    return length_similarity(c1, c2) * counter_cosine_similarity(c1, c2)


# helper functions
def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dot_product = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dot_product / (magA * magB)


def length_similarity(c1, c2):
    lenc1 = sum(c1.itervalues())
    lenc2 = sum(c2.itervalues())
    return min(lenc1, lenc2) / float(max(lenc1, lenc2))