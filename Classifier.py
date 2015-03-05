__author__ = 'jason'
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer


class Classifier:

    def __init__(self, content_type, initial_content):
        self.content_type = content_type    # a string with that describes the type of data to be stored
        self.content = initial_content

    def classify(self, content_type, content):
        if self.content_type != content_type:   # contents do not match
            return -1                           # error

        if content_type == "hashtags":




stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]
