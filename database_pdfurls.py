import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def_pdfurls import PdfUrl
 
engine = create_engine('sqlite:///pdf_urls.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
# Create an artist
pdf_url = PdfUrl("http://www.blah.pdf", False)

 
# Add the record to the session object
session.add(pdf_url)
# commit the record the database
session.commit()
 
# Add several artists

#session.add_all([
#    Artist("MXPX"),
#    Artist("Kutless"),
#    Artist("Thousand Foot Krutch")
#    ])
#session.commit()
