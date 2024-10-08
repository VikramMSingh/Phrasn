from dotenv import load_dotenv
import os

load_dotenv('.env')

class Config(object):
    DEBUG = True
    LANGUAGES = ['en', 'de', 'fr']
    GOOGLE_CLIENT_ID = os.getenv('CID')
    GOOGLE_CLIENT_SECRET = os.getenv('CSK')
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
