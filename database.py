import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import Letters
 
engine = create_engine('sqlite:///shareholder_letters.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
# Create an artist
new_letter = Letters("this is a letter blah blah")

 
# Add the record to the session object
session.add(new_letter)
# commit the record the database
session.commit()
 
# Add several artists

#session.add_all([
#    Artist("MXPX"),
#    Artist("Kutless"),
#    Artist("Thousand Foot Krutch")
#    ])
#session.commit()
