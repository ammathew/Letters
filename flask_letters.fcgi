#!/home2/thezeith/public_html/letters/letters/bin/python

from flup.server.fcgi import WSGIServer
from flask_letters import app as application

WSGIServer(application).run()
