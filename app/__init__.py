from flask import Flask
from config import Config
from firebase_admin import firestore
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
db = firestore.client()
jwt = JWTManager(app)
token_blacklist = set()


from app import routes

