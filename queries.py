# queries.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def_pdfurls import PdfUrl
from table_def import Letters 
from sqlalchemy import distinct
from sqlalchemy import func

engine = create_engine('sqlite:///shareholder_letters.db', echo=True)
#engine = create_engine('sqlite:///pdf_urls.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
# how to do a SELECT * (i.e. all)
res = session.query( Letters ).all()
#res = session.query( PdfUrl ).distinct()
#res = session.query( PdfUrl ).distinct( PdfUrl.pdf_url ).group_by( PdfUrl.pdf_url).filter( PdfUrl.scraped == False ).limit( 50 )
#res = session.query( PdfUrl ).all()
i=0
for item in res:
    i = i + 1
  #  print item.pdf_url
    print i
