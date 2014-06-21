from BeautifulSoup import BeautifulSoup, SoupStrainer
import requests
from xgoogle.search import GoogleSearch, SearchError
import pickle
import simplejson
import re
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import Letters


searchTerms = [ 'shareholder letter', 'letter to shareholders' ]

def getUrls ( searchTerm ):
   links = []
   f = open('output.txt', 'w')
   try:
      gs = GoogleSearch( searchTerm)
      gs.results_per_page = 50
      results = gs.get_results()
      for res in results:
         links.append( res.url.encode("utf8") )
      pickle.dump( links, f )
      f.close()
      return links
   except SearchError, e:
      print "Search failed: %s" % e

def checkWords( links ):
   texts = []
   words = 'richest men'.split(' ')
   for link in links: 
      r = requests.get( link )
      txt= r.text
      sentences = re.findall(r"([^.]*\.)" ,txt)  
      for sentence in sentences:
         if all(word in sentence for word in words):
            texts.append( txt )
   return texts

def addToDb( texts ):
   engine = create_engine('sqlite:///shareholder_letters.db', echo=True)
   Session = sessionmaker(bind=engine)
   session = Session()
   list_to_add = []
   for text in texts:
      aa = Letters( text )
      print aa
      list_to_add.append( Letters( aa ) )
   print "add to list"
   print list_to_add
  # session.add(new_letter)
  # session.commit()   
   
   
             #links = getUrls( 'shareholder letters' )
f = open('output.txt', 'r')
links = pickle.load(f)
print links
texts = checkWords( links )
addToDb( texts )

