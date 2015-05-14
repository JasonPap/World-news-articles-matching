__author__ = 'jason'

from NewsAggregator import NewsAggregator
from NewsArticle import NewsArticle
from XMLparser import *
from nltk.corpus import stopwords

countries = ["Greece"]

aggr = NewsAggregator(0.35)

xmlfiles = ["cbsnews.xml", "Global News.xml", "chathamdailynews.xml", "Sky-News.xml", "npr.xml",
            "whittierdailynews.xml", "dailynews.xml", "galvestondailynews.xml", "cbc.xml", "metro.xml", "Latimes.xml",
            "thestar.xml", "Huffingtonpost.xml", "express.xml", "rte.xml", "nwfdailynews.xml", "irishtimes.xml",
            "zeenews-india.xml", "scrippsobfeeds.xml", "Breaking News.xml", "abcnews.xml", "Independent.xml",
            "Yahoo.xml", "Telegraph.xml", "FOX News.xml", "nbcnews.xml", "news24.xml", "Reuters.xml", "Google.xml",
            "caribbeannewsnow.xml", "The Guardian.xml", "BBC.xml", "CNN.xml", "dailymail.xml", "sciencedaily.xml",
            "tvnz.xml"]

id = 0
for filename in xmlfiles:
    larct = parse(filename)
    for arcticle in larct:
        newarticle = NewsArticle(id, arcticle[1], arcticle[0], arcticle[4], arcticle[2], countries)
        newarticle.extract_metadata()
        aggr.add_article(newarticle)
        print id
        id += 1
        print aggr.topics

print "done"

print aggr.topics

