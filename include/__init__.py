from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = '4a7649d351c052cc24f8f64f3a95f580' # Required for POST requests. Will add this to enviroment variables later.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'   # For testing we will use sqlite3.

app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Database instance
db = SQLAlchemy(app)
# Bcrypt will allow us to hash and verify user passwords.
bcrypt = Bcrypt(app)
# Login manager will allow us to keep track of the user who is currently logged in.
login_manager = LoginManager(app)

from include import routes