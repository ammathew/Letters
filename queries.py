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
for url in res:
    print "this is url id"
    print url.scraped
 
