__author__ = 'jason'
from collections import Counter
import math
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer


# main functions used by others
def list_similarity(list1, list2):
    c1, c2 = Counter(list1), Counter(list2)
    return length_similarity(c1, c2) * counter_cosine_similarity(c1, c2)


def text_similarity(text1, text2):
    return cosine_sim(text1, text2)


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


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


# static objects initialized at start
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')