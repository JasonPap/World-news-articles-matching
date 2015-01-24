__author__ = 'jason'
from textblob import TextBlob
from textblob.np_extractors import FastNPExtractor
from textblob import Word
from hashtagify import Hashtagify
from nltk.tag.stanford import NERTagger


class NewsArticle:
    def __init__(self, title, date, text):
        self.title = title
        self.date = date
        self.text = text
        self.metadata = dict()

    def extract_metadata(self):
        self.extract_noun_phrases()
        self.create_title_hashtags()

    def extract_noun_phrases(self):
        extractor = FastNPExtractor()
        text = TextBlob(self.text, np_extractor=extractor)
        self.metadata["noun_phrases"] = []
        for noun_phrase in text.noun_phrases:
            self.metadata["noun_phrases"].append(noun_phrase)
            w = Word(noun_phrase)
            print noun_phrase
            print w.lemmatize()

    def create_title_hashtags(self):
        ht = Hashtagify(title = self.title, content= self.text)

        # tag the relevant words on the title and save the result
        tagged_title = ht.hashtagify(0.40)
        self.metadata["tagged_title"] = tagged_title

        # get only the tagged words and save them separately
        l_words = tagged_title.split(' ')
        l_tags = []
        for w in l_words:
            if "#" in w:
                l_tags.append(w)
        self.metadata["hashtags"] = l_tags

    def named_entity_extraction(self):
        ner = NERTagger('/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       '/usr/share/stanford-ner/stanford-ner.jar')
        extracted_ne = ner.tag(self.text.split())
        persons = self.process_named_entities(extracted_ne, "PERSON")
        organizations = self.process_named_entities(extracted_ne, "ORGANIZATION")
        locations = self.process_named_entities(extracted_ne, "LOCATION")
        self.metadata["persons"] = persons
        self.metadata["organizations"] = organizations
        self.metadata["locations"] = locations


    @staticmethod
    def process_named_entities(named_entities_l, type):
        aggregated_results = []
        prev_flag = 0
        for named_entity in named_entities_l:
            if named_entity[1] == type and prev_flag == 0:
                aggregated_results.append(named_entity[0])
                prev_flag = 1
            elif named_entity[1] == type and prev_flag == 1:
                aggregated_results[len(aggregated_results) -1] += " " + named_entity[0]
            else:
                prev_flag = 0

        return aggregated_results




print "--start--"
test = NewsArticle("this", "that", "Within hours of acceding to the throne, King Salman, 78, vowed to maintain the same policies as his predecessors.")
test.named_entity_extraction()
print "--end--"