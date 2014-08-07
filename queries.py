# queries.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import Letters
 
engine = create_engine('sqlite:///shareholder_letters.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
# how to do a SELECT * (i.e. all)
search_term = 'Third'
aa =  session.query( Letters ).filter(Letters.letter.like("%\%s\%"%(search_term))).first()
print aa.letter
