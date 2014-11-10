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
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#from app.models import User, Todo

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(250))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
    todos = db.relationship('Todo' , backref='user',lazy='dynamic')

    def __init__(self , username ,password , email):
        self.username = username
        self.set_password(password)
        self.email = email
        self.registered_on = datetime.utcnow()

    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password , password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    done = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False
        self.pub_date = datetime.utcnow()


@app.route('/')
@login_required
def index():
    return render_template('index.html',
        todos=Todo.query.filter_by(user_id = g.user.id).order_by(Todo.pub_date.desc()).all()
    )


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


@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
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
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 

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

@app.route('/database')
def hello_world():
    return render_template('landing.html')

#### DATA VISUALIZATION. TODO: MOVE THIS #######

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAI0xWwAAAAAAh%2BD1hYDRl4VPTQbpDgf68WAn2Ao%3DXf6RD1CSilQbCQufOD0Cn3NsBgfRHcBkMgA0Kdr4ClN29Jfrge"

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


CONSUMER_TOKEN = '5LdbdnyemT8c87Fc5EVFv9VbG'
CONSUMER_SECRET = 'afBHVZFC7nGRX3rQJsIRtpFgLzn1akR0HOLX4gsCn4GiJULWED'
from flask import request
import tweepy
 
#config

CALLBACK_URL = 'http://www.thezeitheist.com/verify'
session = dict()
db = dict() #you can save these values to a database
 
@app.route("/authtwitter")
def send_token():
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, 
                               CONSUMER_SECRET, 
                               CALLBACK_URL)
    
    try: 
		#get the request tokens
        redirect_url= auth.get_authorization_url()
        session['request_token']= (auth.request_token.key,
                                   auth.request_token.secret)
    except tweepy.TweepError:
        print 'Error! Failed to get request token'
        
	#this is twitter's url for authentication
    return flask.redirect(redirect_url)	
 
@app.route("/verify")
def get_verification():
 
	#get the verifier key from the request url
	verifier= request.args['oauth_verifier']
 
	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
	token = session['request_token']
	del session['request_token']
 
	auth.set_request_token(token[0], token[1])
 
	try:
		    auth.get_access_token(verifier)
	except tweepy.TweepError:
		    print 'Error! Failed to get access token.'
 
	#now you have access!
	api = tweepy.API(auth)

	#store in a db
	db['api']=api
	db['access_token_key']=auth.access_token.key
	db['access_token_secret']=auth.access_token.secret
	return flask.redirect(flask.url_for('start'))
 
@app.route("/start")
def start():
	#auth done, app logic can begin
	api = db['api']
 
	#example, print your latest status posts
	return flask.render_template('afterauth.html', tweets=api.user_timeline())


@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    aa = str( type( exception ) )
    aa = traceback.format_exc()
    return aa

if __name__ == '__main__':
    app.run(debug=True)
