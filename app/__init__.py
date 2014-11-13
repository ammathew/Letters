from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__, template_folder="templates" )
app.config.from_object('config')
db = SQLAlchemy(app)
from app import models

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
