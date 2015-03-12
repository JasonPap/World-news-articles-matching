__author__ = 'jason'

from NewsAggregator import NewsAggregator
from NewsArticle import NewsArticle

countries = ["Greece"]

arct1 = NewsArticle(1,"the first article ever", "17/3/2015", "Something happend in Greece when Mr.Aris was drinking his coffe and now everyone is wondering if they should run away.", "http://www.aris.com", countries)
arct2 = NewsArticle(1,"the first article ever", "17/3/2015", "Something happend in Greece when Mr.Aris was drinking his coffe and now everyone is wondering if they should run away.", "http://www.aris.com", countries)

print "done"

aggr = NewsAggregator(0.8)
arct1.extract_metadata()
arct2.extract_metadata()
print "metadata done"

aggr.add_article(arct1)
aggr.add_article(arct2)
print "zuper"
print "duper"