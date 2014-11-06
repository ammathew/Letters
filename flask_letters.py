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

import requests
import csv 

import base64
import json
import httplib
import urllib

from application_only_auth import Client

import pickle

engine = create_engine('sqlite:///shareholder_letters.db', echo=True)

from analyze_sentiment import *
import traceback

import urllib


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

@app.route('/database')
def hello_world():
    return render_template('landing.html')

@app.route('/api/search', methods = ['GET'])
@nocache
def get_tasks():
    Session = sessionmaker(bind=engine)
    session = Session()

    search_term = request.args.get('search_term', 'Third')
    search_term = str( search_term )
    try:
        aa =  session.query( Letters ).filter(Letters.letter.like("%%%s%%"%(search_term))).distinct( Letters.letter ).limit(1000)
        session.close()
        
        shortenedLetters = []
        for item in aa:
            index = item.letter.find( search_term )
            shortenedLetter = item.letter[ index-50:index+50]
            dic = {}
            dic["sletter"] = shortenedLetter
            dic["id"]= item.id 
            shortenedLetters.append( dic )
        
        return jsonify({ "data" : shortenedLetters })
    except:
        return jsonify({ "blah" : "not found" })

#### DATA VISUALIZATION. TODO: MOVE THIS #######

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAI0xWwAAAAAAh%2BD1hYDRl4VPTQbpDgf68WAn2Ao%3DXf6RD1CSilQbCQufOD0Cn3NsBgfRHcBkMgA0Kdr4ClN29Jfrge"

CLASSIFIER = openClassifier()

@app.route('/')
def visualization():
    return make_response( render_template( 'viz.html' ) )

def getSentTimeseries( rawTwitterData ):
    res = json.loads( rawTwitterData )
    res = res["statuses"]
    tweetSentimentTimeseries = []
    for item in res:
        aa = {}
        aa["pos"] = getRating( item["text"], CLASSIFIER );
        aa["created_at"] = item["created_at"]
        aa["text"] = item["text"]
        tweetSentimentTimeseries.append( aa )
    tweetSentimentTimeseries = json.dumps( tweetSentimentTimeseries )
    return tweetSentimentTimeseries

def getPieChartData( rawTwitterData ):
    res = json.loads( rawTwitterData )
    res = res["statuses"]
    aa = {}
    aa["pos"] = 0
    aa["neg"] = 0
    for item in res:
        sent = getRating( item["text"], CLASSIFIER )
        if sent > .5:
            aa["pos"] += 1
        else:
            aa["neg"] +=1
    tweetSentimentTimeseries = []
    for item in res:
        cc = {}
        cc["created_at"] = item["created_at"]
        cc["text"] = item["text"]
        cc["location"] = item["user"]["location"]
        cc["place"] = item["place"]
        cc["pos"] = getRating( item["text"], CLASSIFIER )
        tweetSentimentTimeseries.append( cc )
        
    bb = []
    bb.append( { "key": "pos", "y" : aa["pos"] } )
    bb.append( { "key": "neg", "y" : aa["neg"] } ) 
    bb.append( tweetSentimentTimeseries )
    pieChartData = json.dumps( bb )
    return pieChartData

    
@app.route('/api/get-timeseries', methods = ['GET'])
@nocache
def get_timeseries():
   url = 'http://finance.google.co.uk/finance/historical?q=AAPL&startdate=Oct+1,2012&enddate=Oct+9,2013&output=csv'
   res = requests.get(url)
   prices_csv = res.text.encode('utf-8')

   file = open("temp.csv", "w")
   file.write( prices_csv )
   file.close()

   file = open("temp.csv", "r")
   
   prices = []
   reader = csv.reader( file, delimiter=',')
   for row in reader:
       prices.append( row[4] )

   del prices[0]

   return jsonify({"data": prices })

@app.route('/api/company-info', methods = ['GET'])
def searchCompanyName():
    search_term = request.args.get('search_term')
    search_term = str( search_term+ " -RT" )
    search_term = urllib.quote_plus( search_term )
    geocode = request.args.get('geocode')
    geocode = str( geocode )
    geocode = urllib.quote_plus( geocode )
    
    posts = searchTwitterPosts( search_term, geocode )  

   # sentiment = getSentTimeseries( posts )
    sentiment = getPieChartData( posts )
    return sentiment

def searchTwitterPosts( companyName, geocode  ):
    url='https://api.twitter.com/1.1/search/tweets.json?q=%s&count=100&geocode=%s'%( companyName, geocode )

    #raise Exception( url );

    CONSUMER_KEY = '5LdbdnyemT8c87Fc5EVFv9VbG'
    CONSUMER_SECRET = 'afBHVZFC7nGRX3rQJsIRtpFgLzn1akR0HOLX4gsCn4GiJULWED'

    client = Client(CONSUMER_KEY, CONSUMER_SECRET)

    # Pretty print of tweet payload
    tweet = client.request( url )

    # Show rate limit status for this application
    status = client.rate_limit_status()
    return json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ':'))
  #  return tweet

@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    aa = str( type( exception ) )
    aa = traceback.format_exc()
    return aa

if __name__ == '__main__':
    app.run(debug=True)
