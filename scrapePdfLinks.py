import re
from bs4 import BeautifulSoup
import requests
import urlparse

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def_pdfurls import PdfUrl

import pickle


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import urllib
from table_def import Letters

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
	print 'adding'
	print url
        links = scrapePdfUrls( url )
        addLinksListToDB( links )


def convert_pdf_to_txt( path ):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    
    fp = urllib.urlretrieve( path )
    fp = open( fp[0], 'rb')
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
    unicodeString = unicode( str, "utf-8")
    return unicodeString

def addPdfToDB( pdfStr ):
    engine = create_engine('sqlite:///shareholder_letters.db', echo=True)
    Session = sessionmaker(bind=engine)
    session_letters = Session()
    new_letter = Letters( pdfStr )
    session_letters.add(new_letter)
    session_letters.commit()

from table_def_pdfurls import PdfUrl
from sqlalchemy import update

def startScraping():
    engine = create_engine('sqlite:///pdf_urls.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    pdfUrls = session.query(PdfUrl).all()
    
    for pdf_url in pdfUrls:
        try:
            print pdf_url.pdf_url
            pdfStr = convert_pdf_to_txt( pdf_url.pdf_url )
            addPdfToDB( pdfStr )
            pdf_url.scraped = True
            session.add( pdf_url )
            print pdf_url.scraped
            session.commit()
        except:
            pass
            

#url = "http://www.thirdavenuecapitalplc.com/ucits/shareholder-letters.asp"
#links = scrapePdfUrls( url )
#addLinksListToDB( links )
aa( 'urls_page_2.txt' )

#test_remote_pdf = 'http://www.thirdavenuecapitalplc.com/ucits/docs/shareholderletters/Q4%202013%20UCITS%20Letters.pdf'
#pdfStr = convert_pdf_to_txt( test_remote_pdf  )

#addPdfToDB( pdfStr )

#startScraping()
