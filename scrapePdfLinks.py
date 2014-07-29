import re
from bs4 import BeautifulSoup
import requests
import urlparse

# parse page content
url = "http://www.thirdavenuecapitalplc.com/ucits/shareholder-letters.asp"
def scrapePdfUrls( url ):
    match = re.compile('\.(pdf)')
    page = requests.get( url )
    page = BeautifulSoup(page.text)

    # check links
    for link in page.findAll('a'):
        try:
            href = link['href']
            if re.search(match, href):
                link = urlparse.urljoin(url, href)
                print link
        except KeyError:
            pass

scrapePdfUrls( url )
