# queries.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def_pdfurls import PdfUrl
 
engine = create_engine('sqlite:///pdf_urls.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
# how to do a SELECT * (i.e. all)
res = session.query(PdfUrl).count()
print "this is count"
print res
#for pdf_url in res:
#    print pdf_url.pdf_url
#    print pdf_url.scraped
 
