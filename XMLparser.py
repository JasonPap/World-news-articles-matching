#!/usr/bin/python

import xml.sax
from xml.dom.minidom import parse
import xml.dom.minidom

class ArticleHandler( xml.sax.ContentHandler ):
	def __init__(self):
		self.CurrentData = ""
		self.date = ""
		self.title = ""
		self.link = ""
		self.description = ""
		self.mainbody = ""

	# Call when an element starts
	def startElement(self, tag, attributes):
		self.CurrentData = tag
		if tag == "id":
			print "*****Article*****"
			id = attributes["id"]
			print "id:", id

	# Call when an elements ends
	def endElement(self, tag):
		if self.CurrentData == "date":
			print "Date:", self.date
		elif self.CurrentData == "title":
			print "Title:", self.title
		elif self.CurrentData == "link":
			print "Link:", self.link
		elif self.CurrentData == "description":
			print "Description:", self.description
		elif self.CurrentData == "mainbody":
			print "Mainbody:", self.mainbody
		self.CurrentData = ""

	# Call when a character is read
	def characters(self, content):
		if self.CurrentData == "date":
			self.date = content
		elif self.CurrentData == "title":
			self.title = content
		elif self.CurrentData == "link":
			self.link = content
		elif self.CurrentData == "description":
			self.description = content
		elif self.CurrentData == "mainbody":
			self.mainbody = content

print "xa"
# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("News/Independent.xml")
collection = DOMTree.documentElement
if collection.hasAttribute("name"):
	print "Root element : %s" % collection.getAttribute("name")

# Get all the Articles of the Site
articles = collection.getElementsByTagName("Article")

# Print detail of each Article.
for article in articles:
	print "*****Article*****"
	
	#ID
	if article.hasAttribute("id"):
		print "ID: %s" % article.getAttribute("id")

	#DATE
	date = article.getElementsByTagName('date')[0]
	if len(date.childNodes) == 0:
		print "Date: %s" % ""
	else:
		print "Date: %s" % date.childNodes[0].data
	
	#TITLE
	title = article.getElementsByTagName('title')[0]
	if len(title.childNodes) == 0:
		print "Title: %s" % ""
	else:
		print "Title: %s" % title.childNodes[0].data
	
	#LINK
	Link = article.getElementsByTagName('Link')[0]
	if len(Link.childNodes) == 0:
		print "Link: %s" % ""
	else:
		print "Link: %s" % Link.childNodes[0].data
	
	#DESCRIPTION
	Description = article.getElementsByTagName('Description')[0]
	if len(Description.childNodes) == 0:
		print "Description: %s" % ""
	else:
		print "Description: %s" % Description.childNodes[0].data
	
	#MAINBODY
	MainBody = article.getElementsByTagName('MainBody')[0]
	if len(MainBody.childNodes) == 0:
		print "MainBody: %s" % ""
	else:
		print "MainBody: %s" % MainBody.childNodes[0].data
	
	
	
