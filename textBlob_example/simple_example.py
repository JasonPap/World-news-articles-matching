__author__ = 'jason'

#from textblob import TextBlob

#wiki = TextBlob("Python is a high-level, general-purpose programming language.")
#print wiki.tags
#print wiki.noun_phrases
#print wiki.sentiment

from nltk.tag.stanford import NERTagger

st = NERTagger('/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', '/usr/share/stanford-ner/stanford-ner.jar')
s = "Rami Eid is studying at Stony Brook University in NY"
print s
l = st.tag(["Rami Eid is studying at Stony Brook University in Brooklyn, NYC"])
print l

