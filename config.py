import os
import firebase_admin
from firebase_admin import credentials

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    CRED = credentials.Certificate("app/serviceAccountKey.json")
    firebase_admin.initialize_app(CRED)

    JWT_SECRET_KEY = str(os.environ.get('JWT_SECRET'))