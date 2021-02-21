from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
# todo: search for engine in sqlalchemy
# this is for slq server


# todo: get username and password, driver, datbase, server to connect to sqlServer
# step 1: connecting to database




app = Flask(__name__)
# this is important for using session
app.secret_key = 'muha'  # make it something complicated

# timeout for remembering the session data, by default
app.permanent_session_lifetime = timedelta(hours=6)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WebDomain.db'
# to ignore warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from WebDomains import routes
