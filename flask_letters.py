from datetime import datetime
from flask import Flask, request, jsonify, render_template

from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime

import flask

import sys
sys.path.insert(0, "/home2/thezeith/opt/python27/lib/python2.7/site-packages/" )

app = flask.Flask(__name__)

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import Letters
 


engine = create_engine('sqlite:///shareholder_letters.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)

@app.route('/')
def hello_world():
    return render_template('landing.html')

@app.route('/api/search', methods = ['GET'])
@nocache
def get_tasks():
    search_term = request.args.get('search_term', 'Third')
    search_term = str( search_term )
    try:
        aa =  session.query( Letters ).filter(Letters.letter.like("%%%s%%"%(search_term))).limit(10)
        session.close()
        bb = []
        
        for item in aa:
            bb.append( item.letter )
        return jsonify({ "blah" : bb })
    except:
        return jsonify({ "blah" : "not found" })
  

if __name__ == '__main__':
    app.run(debug=True)
