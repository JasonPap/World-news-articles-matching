__author__ = 'jason'
from textblob import TextBlob
from textblob.np_extractors import FastNPExtractor
from textblob import Word
from hashtagify import Hashtagify
from nltk.tag.stanford import NERTagger
from geonames import *

countryDict = {'AR': "AR"}


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

        general_locations = self.enrich_location(extracted_ne)

    @staticmethod
    def enrich_location(named_entities_l):
        # rules:    LOCATION in LOCATION
        #           LOCATION of LOCATION
        #           LOCATION , LOCATION     note: second location must be a country or a state
        aggregated_results = []
        unified_locations = []

        # if there are less than 3 items in the list, no pattern can be matched
        if len(named_entities_l) < 3:
            return aggregated_results

        for index in range(len(named_entities_l) - 2):
            if named_entities_l[index][1] == "LOCATION" and \
               named_entities_l[index + 1][0].lower() == "in" and \
               named_entities_l[index + 2][1] == "LOCATION":        # first rule matches
                unified_locations.append(named_entities_l[index][0] + named_entities_l[index + 2][0])
            elif named_entities_l[index][1] == "LOCATION" and \
                named_entities_l[index + 1][0].lower() == "of" and \
                named_entities_l[index + 2][1] == "LOCATION":        # second rule matches

                unified_locations.append(named_entities_l[index][0] + named_entities_l[index + 2][0])

            elif named_entities_l[index][1] == "LOCATION" and named_entities_l[index + 1][0].lower() == "," and \
                    named_entities_l[index + 2][1] == "LOCATION" and \
                    isCountry(named_entities_l[index + 2][0]):        # third rule matches

                unified_locations.append(named_entities_l[index][0] + named_entities_l[index + 2][0])

        for location in unified_locations:
            results = search("q=" + location)   # get dictionary with geonames webAPI results
            hierarchy = None
            if "geonameId" in results:
                hierarchy = get_hierarchy(results["geonameId"]) # get dictionary with geonames webAPI results

            # do something to fill the aggregated results list

        return aggregated_results


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


def isCountry(c):
    if c in countryDict:
        return True
    else:
        return False


print "--start--"
test = NewsArticle("this", "that", "Within hours of acceding to the throne, King Salman, 78, vowed to maintain the same policies as his predecessors.")
test.named_entity_extraction()
print "--end--"