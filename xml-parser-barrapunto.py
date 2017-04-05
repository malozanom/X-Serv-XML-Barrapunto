#!/usr/bin/python
# -*- coding: utf-8 -*-

# Simple XML parser for the RSS channel from BarraPunto.
# Miguel Ángel Lozano Montero.

# Prints and stores in a HTML file the news (and urls) in BarraPunto.com,
# after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib.request


class myContentHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.title = ""
        self.link = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = "Title: " + self.theContent + "."
                print(self.title)
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = " Link: " + self.theContent + "."
                htmlFile.write("<a href=" + self.theContent + ">" +
                               self.title + "</a><br>\n")
                print(self.link)
                self.inContent = False
                self.theContent = ""
                self.title = ""
                self.link = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

page = urllib.request.urlopen('http://barrapunto.com/index.rss')
html = (page.read()).decode('utf-8')
rssFile = open("barrapunto.rss", "w")
rssFile.write(html)
rssFile.close()

htmlFile = open("barrapunto.html", "w")
htmlFile.write("<head><meta http-equiv='Content-Type' content='text/html;" +
               "charset=utf-8'/></head><br>\n")

xmlFile = open("barrapunto.rss", "r")
theParser.parse(xmlFile)

htmlFile.close()

print("Parse complete")
