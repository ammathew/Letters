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
 
    #----------------------------------------------------------------------
    def __init__(self, letter):
        """"""
        self.letter = letter    
 
# create tables

Base.metadata.create_all(engine)
