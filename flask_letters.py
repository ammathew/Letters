#!/usr/bin/env python
from datetime import datetime
from flask import Flask, request, jsonify, render_template

from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime

import flask

import sys
sys.path.insert(0, "/home2/thezeith/opt/python27/lib/python2.7/site-packages/" )

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

from analyze_sentiment import *
import traceback

import urllib
import os

from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import login_user , logout_user , current_user , login_required
#from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db, login_manager, BASE_URL
from app.models import User, Todo, TwitterAuth

import json

import nltk


@app.route('/')
def index():
    return render_template('marketing.html')

#@app.route('/')
#@login_required
#def index():
#    return render_template('index.html',
#        todos=Todo.query.filter_by(user_id = g.user.id).order_by(Todo.pub_date.desc()).all()
#    )

@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Title is required', 'error')
        elif not request.form['text']:
            flash('Text is required', 'error')
        else:
            todo = Todo(request.form['title'], request.form['text'])
            todo.user = g.user
            db.session.add(todo)
            db.session.commit()
            flash('Todo item was successfully created')
            return redirect(url_for('index'))
    return render_template('new.html')

@app.route('/todos/<int:todo_id>', methods = ['GET' , 'POST'])
@login_required
def show_or_update(todo_id):
    todo_item = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template('view.html',todo=todo_item)
    if todo_item.user.id == g.user.id:
        todo_item.title = request.form['title']
        todo_item.text  = request.form['text']
        todo_item.done  = ('done.%d' % todo_id) in request.form
        db.session.commit()
        return redirect(url_for('index'))
    flash('You are not authorized to edit this todo item','error')
    return redirect(url_for('show_or_update',todo_id=todo_id))


@app.route('/api/register' , methods=['GET','POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    user = User( username, password, email )
    db.session.add(user)
    db.session.commit()
    return '{ "status" : 200 }'

@app.route('/api/login',methods=['GET','POST'])
def login():    
    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        flash('Username is invalid' , 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid','error')
        return redirect(url_for('login'))
    login_user(registered_user, remember = remember_me)
    #   flash('Logged in successfully')
    return '{ "status" : 200 }'

@app.route('/api/logout')
def logout():
    logout_user()
    return '{ "status" : 200 }'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

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


#### DATA VISUALIZATION. TODO: MOVE THIS #######

#BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAI0xWwAAAAAAh%2BD1hYDRl4VPTQbpDgf68WAn2Ao%3DXf6RD1CSilQbCQufOD0Cn3NsBgfRHcBkMgA0Kdr4ClN29Jfrge"

#CLASSIFIER = openClassifier()


#@app.route('/')
#def visualization():
#    return make_response( render_template( 'viz.html' ) )

#def getSentTimeseries( rawTwitterData ):
#    res = json.loads( rawTwitterData )
#    res = res["statuses"]
#    tweetSentimentTimeseries = []
#    for item in res:
#        aa = {}
#        aa["pos"] = getRating( item["text"], CLASSIFIER );
#        aa["created_at"] = item["created_at"]
#        aa["text"] = item["text"]
#        tweetSentimentTimeseries.append( aa )
#    tweetSentimentTimeseries = json.dumps( tweetSentimentTimeseries )
#    return tweetSentimentTimeseries

#def getPieChartData( rawTwitterData ):
#    res = json.loads( rawTwitterData )
#    res = res["statuses"]
#    aa = {}
#    aa["pos"] = 0
#    aa["neg"] = 0
#    for item in res:
#        sent = getRating( item["text"], CLASSIFIER )
#        if sent > .5:
#            aa["pos"] += 1
#        else:
#            aa["neg"] +=1
#    tweetSentimentTimeseries = []
#    for item in res:
#        cc = {}
#        cc["created_at"] = item["created_at"]
#        cc["text"] = item["text"]
#        cc["location"] = item["user"]["location"]
#        cc["place"] = item["place"]
#        cc["pos"] = getRating( item["text"], CLASSIFIER )
#        tweetSentimentTimeseries.append( cc )

#    bb = []
#    bb.append( { "key": "pos", "y" : aa["pos"] } )
#    bb.append( { "key": "neg", "y" : aa["neg"] } ) 
#    bb.append( tweetSentimentTimeseries )
#    pieChartData = json.dumps( bb )
#    return pieChartData


#@app.route('/api/company-info', methods = ['GET'])
#def searchCompanyName():
#    search_term = request.args.get('search_term')
#    search_term = str( search_term+ " -RT" )
#    search_term = urllib.quote_plus( search_term )
#    geocode = request.args.get('geocode')
#    geocode = str( geocode )
#    geocode = urllib.quote_plus( geocode )
    
#    posts = searchTwitterPosts( search_term, geocode )  

   # sentiment = getSentTimeseries( posts )
 #   sentiment = getPieChartData( posts )
 #   return sentiment

#def searchTwitterPosts( companyName, geocode  ):
#    url='https://api.twitter.com/1.1/search/tweets.json?q=%s&count=100&geocode=%s'%( companyName, geocode )

#    #raise Exception( url );

#    client = Client(CONSUMER_KEY, CONSUMER_SECRET)

    # Pretty print of tweet payload
#    tweet = client.request( url )

    # Show rate limit status for this application
#    status = client.rate_limit_status()
#    return json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ':'))
#    return tweet


CONSUMER_TOKEN = 'QBwtZvA52I6qz5ayobHrkjPnd'
CONSUMER_SECRET = 'xecOS9Wdc4jAbfOycu5WnKHjElEXKp1XfdRqKwMh8khoK2bnFe'
#CONSUMER_TOKEN = '5LdbdnyemT8c87Fc5EVFv9VbG'
#CONSUMER_SECRET = 'afBHVZFC7nGRX3rQJsIRtpFgLzn1akR0HOLX4gsCn4GiJULWED'
from flask import request
import tweepy
CALLBACK_URL = 'http://www.thezeitheist.com/verify'
auth_twitter_session = dict()
db_twitter = dict() #you can save these values to a database
TWITTER_API = None 

@app.route("/api/authtwitter",  methods = ['POST', 'GET'] )
def send_token():
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, 
                               CONSUMER_SECRET, 
                               CALLBACK_URL)
    
    try: 
		#get the request tokens
        redirect_url= auth.get_authorization_url()
        auth_twitter_session['request_token']= (auth.request_token.key,
                                   auth.request_token.secret)
    except tweepy.TweepError:
        print 'Error! Failed to get request token'
        
	#this is twitter's url for authentication

    data = { 'redirect_url' : redirect_url }
    data = json.dumps( data )

    return data
 
@app.route("/verify")
def get_verification():
    verifier= request.args['oauth_verifier']
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    #  raise Exception(  auth_twitter_session['request_token'] )
    token = auth_twitter_session['request_token']
    del auth_twitter_session['request_token']
    auth.set_request_token(token[0], token[1])
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'
        
    twitter_auth = TwitterAuth( auth.access_token.key, auth.access_token.secret, g.user.id )
    db.session.add( twitter_auth )
    db.session.commit()
    return redirect( BASE_URL + '/#/dashboard')
   # return flask.render_template('index.html')
 
@app.route("/api/twitterPosts")
def start():
    global TWITTER_API
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    twitter_auth  = TwitterAuth.query.filter( TwitterAuth.user_id == g.user.id ).first() 
    auth.set_access_token( twitter_auth.access_token_key, twitter_auth.access_token_secret)
    TWITTER_API = tweepy.API(auth, parser=tweepy.parsers.JSONParser() )
    tweets=TWITTER_API.user_timeline();
    data = json.dumps( tweets );
    return data

def twitterApi():
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    twitter_auth  = TwitterAuth.query.filter( TwitterAuth.user_id == g.user.id ).first() 
    auth.set_access_token( twitter_auth.access_token_key, twitter_auth.access_token_secret)
    TWITTER_API = tweepy.API(auth, parser=tweepy.parsers.JSONParser() )
    return TWITTER_API

@app.route("/api/twitter/favorite/create", methods=['GET', 'POST'])
def createFavorite():
    req = request.get_json()
    id = req['id']
    twitterAPI = twitterApi()
    data = twitterAPI.create_favorite( id )
    data = json.dumps( data )
    return data

@app.route("/api/twitter/update_status", methods=['GET', 'POST'])
def replyToTweet():
    req = request.get_json()
    status = req['status']
    in_reply_to_status_id = req['in_reply_to_status_id']
    twitterAPI = twitterApi()
  #  raise Exception( in_reply_to_status_id )
    data = twitterAPI.update_status( status, in_reply_to_status_id=in_reply_to_status_id )
    data = json.dumps( data )
    return data

@app.route("/api/searchTwitter", methods=['GET', 'POST'])
def searchTwitter():
    searchTerm = request.args['search_term']

    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    twitter_auth  = TwitterAuth.query.filter( TwitterAuth.user_id == g.user.id ).first() 
    auth.set_access_token( twitter_auth.access_token_key, twitter_auth.access_token_secret)

    TWITTER_API = tweepy.API(auth, parser=tweepy.parsers.JSONParser() )
    data = TWITTER_API.search( searchTerm )
    data = json.dumps( data )
    return data

@app.route("/api/twitter/convos", methods=['GET', 'POST'])
def mentions():
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    twitter_auth  = TwitterAuth.query.filter( TwitterAuth.user_id == g.user.id ).first() 
    auth.set_access_token( twitter_auth.access_token_key, twitter_auth.access_token_secret)

    TWITTER_API = tweepy.API(auth, parser=tweepy.parsers.JSONParser() )
    mentions = TWITTER_API.mentions_timeline()
    
    convos = []

    for item in mentions:
        if item['in_reply_to_status_id_str']:
            convos.append( item )
 
    convo_superset = create_superset( convos )
   
    data = json.dumps( convo_superset )
    return data

def create_superset( convos ):
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    twitter_auth  = TwitterAuth.query.filter( TwitterAuth.user_id == g.user.id ).first() 
    auth.set_access_token( twitter_auth.access_token_key, twitter_auth.access_token_secret)
    TWITTER_API = tweepy.API(auth, parser=tweepy.parsers.JSONParser() )
    
    convo_superset = []

    for item in convos:
        convo = []
        convo.append( item )
        in_reply_to_status_id_str = item['in_reply_to_status_id_str']
        while in_reply_to_status_id_str:
            status = TWITTER_API.get_status( in_reply_to_status_id_str )
            convo.append( status )
            in_reply_to_status_id_str = status['in_reply_to_status_id_str']
        convo_superset.append( convo )

    return convo_superset
    
        
        

@app.route("/api/extractEnts", methods=['GET', 'POST'] )
def extract_entities():
    req = request.get_json()
    text = req['text']
    entities = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'node'):
                for c in chunk.leaves():
                    entities.append( c[0] )
    data = json.dumps( entities )
    return data

@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    aa = str( type( exception ) )
    aa = traceback.format_exc()
    return aa

if __name__ == '__main__':
    app.run(debug=True)
