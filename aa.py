#from BeautifulSoup import BeautifulSoup, SoupStrainer
import requests
from xgoogle.search import GoogleSearch, SearchError
from xgoogle.googlesets import GoogleSets, LARGE_SET, SMALL_SET

import pickle
import re
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import Letters
import urllib
#import scraperwiki
import pdfminer


pdf_url = 'http://www.sec.gov/divisions/investment/13f/13flist2013q4.pdf'

searchTerms = [ 'shareholder letter', 'letter to shareholders' ]


def getUrls2( page_num ):
   gs = GoogleSearch('shareholder letter')
   gs.results_per_page = 50
   gs.page = page_num
   results = gs.get_results()
   for item in results:
      print item.url.encode("utf8")
   



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
   
   
def getSearchResultsByPageNum( search_term, start_num_end_num ):
   num = start_num
   end = end_num
   while ( num < end ):
      links = getUrls( 'shareholder letters', start )
      num = num + 1
   
   #f = open('output.txt', 'r')
   #links = pickle.load(f)

#print links
#texts = checkWords( links )
#addToDb( texts )

#print "HELLO"
#path = '13flist2013q4.pdf'

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    
    fp = urllib.urlretrieve( path )
    fp = open( fp[0], 'rb')
    print fp
    print dir( fp )
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

#test_url = 'http://www.thirdavenuecapitalplc.com/ucits/shareholder-letters.asp'
#test_remote_pdf = 'http://www.thirdavenuecapitalplc.com/ucits/docs/shareholderletters/Q4%202013%20UCITS%20Letters.pdf'

#convert_pdf_to_txt(test_remote_pdf)

getUrls2( 11 )
