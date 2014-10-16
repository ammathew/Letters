# table_def.py
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///shareholder_letters.db', echo=True)
Base = declarative_base()
 
########################################################################
class Letters(Base):
    
    __tablename__ = "letters"
 
    id = Column(Integer, primary_key=True)
    letter = Column(TEXT)  
    url_id = Column(Integer)
 
    #----------------------------------------------------------------------
    def __init__(self, letter, url_id):
        """"""
        self.letter = letter    
        self.url_id = url_id

# create tables

Base.metadata.create_all(engine)
