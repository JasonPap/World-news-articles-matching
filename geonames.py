__author__ = 'jason'


def geo_search(query):
    results = dict()
    # use the geonames webAPI to fill dictionary with data
    results["country"] = "Greece"

    return results


import urllib2
from bs4 import BeautifulSoup

def getCountry(town):

    url = "http://api.geonames.org/search?q=" + town.replace(" ","%20") + "&maxRows=1&username=project0&password=jasonaris"
    response = urllib2.urlopen(url)
    page_source = response.read()

    soup = BeautifulSoup(page_source)
    countryname = str(soup.find('countryname'))

    if countryname is None:
        result = None
    else:
        result = countryname.replace("<countryname>","").replace("</countryname>","")

    return result

print getCountry("kalithea")
