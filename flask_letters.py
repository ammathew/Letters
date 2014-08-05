from datetime import datetime
from flask import Flask, request, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import Letters

app = Flask(__name__)

engine = create_engine('sqlite:///shareholder_letters.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/the-time')
def the_time():
     cur_time = str(datetime.now())
     return cur_time + ' is the current time!  ...YEAH!'

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/api/search', methods = ['GET'])
def get_tasks():
  #  search_term = request.args.get('search_term')
  #  aa =  session.query( Letters ).filter(Letters.letter.like("%%s%"%(search_term))).first()
  #  return jsonify( { 'the_term_was' : aa.letter } )
    return jsonify( { 'tasks': 'asdfdas' } )


if __name__ == '__main__':
    app.run()
