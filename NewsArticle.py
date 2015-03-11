__author__ = 'jason'
from textblob import TextBlob
from textblob.np_extractors import FastNPExtractor
from hashtagify import Hashtagify
from nltk.tag.stanford import NERTagger
from geonames import *


class NewsArticle:
    def __init__(self, id, title, date, text, url, countries):
        self.id = id
        self.title = title
        self.date = date
        self.text = text
        self.url = url
        self.metadata = dict()
        self.countries = countries

    def extract_metadata(self):
        self.extract_noun_phrases()
        self.create_title_hashtags()
        self.named_entity_extraction()

    def extract_noun_phrases(self):
        extractor = FastNPExtractor()
        text = TextBlob(self.text, np_extractor=extractor)
        self.metadata["noun_phrases"] = []
        for noun_phrase in text.noun_phrases:
            self.metadata["noun_phrases"].append(noun_phrase)

    def create_title_hashtags(self):
        ht = Hashtagify(title=self.title, content=self.text)

        # tag the relevant words on the title and save the result
        tagged_title = ht.hashtagify(0.40)
        self.metadata["title"] = self.title

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
        extracted_ne = ner.tag(self.text.replace(".", "*").replace("!", "*").replace("?", "*").split())

        persons = self.process_named_entities(extracted_ne, "PERSON")
        organizations = self.process_named_entities(extracted_ne, "ORGANIZATION")
        locations = self.unify_locations(extracted_ne)

        self.metadata["persons"] = persons
        self.metadata["organizations"] = organizations
        self.metadata["locations"] = locations

        general_locations = self.enrich_location(locations)
        self.metadata["countries"] = general_locations[0]   # a list of countries
        self.metadata["places"] = general_locations[1]      # a list of places

        useful_ne = self.remove_unwanted_words(extracted_ne)
        self.metadata["summary"] = useful_ne

    def process_named_entities(self, named_entities_l, type):
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

    def is_country(self, c):
        if c in self.countries:
            return True
        else:
            return False

    def unify_locations(self, named_entities):
        # rules:    LOCATION in LOCATION
        #           LOCATION of LOCATION
        #           LOCATION , LOCATION     note: second location must be a country or a state
        #           LOCATION LOCATION
        #           LOCATION
        # return list with unified locations
        unified_locations = []

        # if there are less than 3 items in the list, no pattern can be matched
        if len(named_entities) < 3:
            return None

        index = 0
        while index < len(named_entities) - 2:
            if named_entities[index][1] == "LOCATION" and \
               named_entities[index + 1][0].lower() == "in" and \
               named_entities[index + 2][1] == "LOCATION":        # first rule matches
                unified_locations.append(named_entities[index][0] + named_entities[index + 2][0])
                index += 3

            elif named_entities[index][1] == "LOCATION" and \
                named_entities[index + 1][0].lower() == "of" and \
                named_entities[index + 2][1] == "LOCATION":        # second rule matches

                unified_locations.append(named_entities[index][0] + named_entities[index + 2][0])
                index += 3

            elif named_entities[index][1] == "LOCATION" and named_entities[index + 1][0].lower() == "," and \
                    named_entities[index + 2][1] == "LOCATION" and \
                    self.is_country(named_entities[index + 2][0]):        # third rule matches

                unified_locations.append(named_entities[index][0] + named_entities[index + 2][0])
                index += 3

            elif named_entities[index][1] == "LOCATION" and named_entities[index + 1][1] == "LOCATION":
                                                                    # forth rule matches
                unified_locations.append(named_entities[index][0] + named_entities[index + 1][0])
                index += 2

            elif named_entities[index][1] == "LOCATION":
                                                                    # fifth rule matches
                unified_locations.append(named_entities[index][0])
                index += 1
            else:
                index += 1

        return unified_locations

#    def remove_unwanted_words(self, named_entities):
#        for u_word in self.unwanted_words:
#            named_entities = [(w, pos) for w, pos in named_entities if w != u_word]
#        return named_entities

    def enrich_location(self, unified_locations):
        # return tuple with two lists (countries, places)
        # where each list have the countries and the places found with geo_names API
        l_places = []
        l_countries = []
        for location in unified_locations:
            results = geo_search("q=" + location)   # get dictionary with geonames webAPI results
            if "country" in results:
                l_countries.append(results["country"])

            if "place" in results:
                l_places.append(results["place"])

        aggregated_results = l_countries, l_places

        return aggregated_results




print "--start--"
text = """
A video file posted online Tuesday purports to relay a new message from Japanese ISIS hostage Kenji Goto: He and a captive Jordanian military pilot will be killed in the next 24 hours if Jordan doesn't release a convicted would-be suicide bomber.

It is the second purported message from Goto in four days. If authentic, it is the first time ISIS is publicly linking the fates of Goto and the captive Jordanian pilot, Moaz al-Kassasbeh, whom ISIS captured after his jet crashed last month in Syria.

The latest file, posted Tuesday morning to YouTube and distributed on social media by known ISIS supporters, appears to show a static image of Goto, alone, in handcuffs and wearing orange, holding a picture of who appears to be al-Kassasbeh.

Over the image, a voice purporting to be Goto's restates Saturday's apparent ISIS proposal: Goto would go free if Jordan releases longtime prisoner Sajida al-Rishawi.

This time, it's still a one-for-one swap, but now both the lives of Goto and the Jordanian pilot are threatened if it doesn't go through. CNN cannot independently verify the authenticity of Tuesday's message.



"I've been told this is my last message, and I've also been told that the barrier obstructing my freedom is now just the Jordanian government delaying the handover of Sajida," the voice says in English in Tuesday's post. "Tell the Japanese government to put all the political pressure on Jordan."

"Her for me -- a straight exchange," the voice says. "Any more delays by the Jordanian government will mean they are responsible for the death of their pilot, which will then be followed by mine.

"I only have 24 hours left to live, and the pilot has even less."


Video is similar to earlier post


The nearly two-minute video, posted Tuesday morning ET, makes no mention of releasing pilot al-Kassasbeh, even if al-Rishawi is released.

The video is similar to a post from Saturday, which alleged that ISIS had killed a different Japanese hostage, Haruna Yukawa.

Saturday's post shows a static image of Goto, holding what appears to be a photo of beheaded compatriot Yukaka. A voice, purporting to be Goto's, says that Yukawa was killed because Japan hadn't answered a previous ISIS demand of $200 million for the Japanese captives' freedom.

Saturday's voice also said that the captors no longer demanded money, but rather a Goto-for-al-Rishawi swap.

Japanese Prime Minister Shinzo Abe said Sunday that experts were analyzing Saturday's video, but that it seemed "highly credible." U.S. authorities said they had no reason to doubt its authenticity.


A convicted terrorist, a Jordanian pilot and a Japanese journalist


Al-Rishawi is an Iraqi woman facing the death penalty in Jordan for her role in a series of bombings that killed dozens of people at hotels in the Arab kingdom in 2005. Authorities said she tried to take part in the massacre, but her explosives failed.

Militants say they captured al-Kassasbeh, the Jordanian pilot, after he ejected from his crashing F-16 last month, having taken part in U.S.-led coalition airstrikes near ISIS' de-facto capital, Raqqa, Syria.

Jordan is participating in an American-led mission against ISIS, an organization seeking to establish a caliphate, or Islamic State, and has wrested territory spanning from central Syria to about 100 kilometers (62 miles) north of Baghdad.

Goto, 47, and Yukawa, 42, had gone to the Middle East for different reasons, the former is an experienced freelance journalist covering the conflict in Iraq and Syria, and the latter an aspiring security contractor who felt at home in the war-torn region. They ended up in the hands of ISIS in recent months.
"""
test = NewsArticle(1, "New apparent ISIS post threatens Japanese hostage, Jordanian pilot", "that", text)
test.named_entity_extraction()
print "--end--"