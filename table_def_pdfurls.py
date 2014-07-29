# table_def.py
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///pdf_urls.db', echo=True)
Base = declarative_base()
 
########################################################################
class PdfUrl(Base):
    
    __tablename__ = "pdf_urls"
 
    id = Column(Integer, primary_key=True)
    pdf_url = Column(String)  
    scraped = Column(Boolean, default=False)

    #----------------------------------------------------------------------
    def __init__(self, pdf_url, scraped):
        """"""
        self.pdf_url = pdf_url
        self.scraped = scraped
        
 
# create tables

Base.metadata.create_all(engine)
