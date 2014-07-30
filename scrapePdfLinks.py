import re
from bs4 import BeautifulSoup
import requests
import urlparse

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def_pdfurls import PdfUrl

import pickle

def scrapePdfUrls( url ):
    match = re.compile('\.(pdf)')
    page = requests.get( url )
    page = BeautifulSoup(page.text)
    links = []

    # check links
    for link in page.findAll('a'):
        try:
            href = link['href']
            if re.search(match, href):
                link = urlparse.urljoin(url, href)
                links.append( link ) 
        except KeyError:
            pass

    return links

def addLinksListToDB( links ):
    engine = create_engine('sqlite:///pdf_urls.db', echo=True)
 
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    addToDB = [] 
    for item in links:
        dbItem = PdfUrl( item, False )
        addToDB.append( dbItem ) 

    session.add_all( addToDB )
    session.commit()
        
# take txt file, open, return list

def aa( fileName ):
    urls = pickle.load( open( fileName, 'rb' ) )
    for url in urls:
        links = scrapePdfUrls( url )
        addLinksListToDB( links )

    

#url = "http://www.thirdavenuecapitalplc.com/ucits/shareholder-letters.asp"
#links = scrapePdfUrls( url )
#addLinksListToDB( links )

print aa( 'urls_page_1.txt' )

