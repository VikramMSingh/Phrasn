from flask import Flask, render_template, request, Blueprint, abort
from flask_babel import Babel
from flask_session import Session
from flask_cors import CORS
import sys
import os
from datetime import timedelta
from authlib.integrations.flask_client import *
from flask_wtf.csrf import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
import logging



app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app.secret_key = '4345'
app.config.from_object(Config)
csrf=CSRFProtect()
csrf.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SDU')
db = SQLAlchemy(app)
Migrate(app,db)
load_dotenv('.env')
app.config['KEY'] = os.getenv('KY')
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=60)
app.config['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('JSON_FILE')
oauth = OAuth(app)
#oauth.init_app(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    #authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    #access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    client_kwargs={'scope': 'openid email profile','jwt_iss': 'https://accounts.google.com'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
    )
babel = Babel(app)
Session(app)

def get_locale():
    # Get the user's preferred language from the session if set, otherwise default to 'en'
    return session.get('lang', 'en')

@app.context_processor
def inject_locale():
    return dict(get_locale=get_locale)

babel.init_app(app, locale_selector=get_locale)

from api.routes import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
