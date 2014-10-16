# queries.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def_pdfurls import PdfUrl
 
engine = create_engine('sqlite:///pdf_urls.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
# how to do a SELECT * (i.e. all)
res = session.query(PdfUrl).all()
print "this is count"
for item in res:
    if item.scraped == False:
        print item.id

#for pdf_url in res:
#    print pdf_url.pdf_url
#    print pdf_url.scraped
