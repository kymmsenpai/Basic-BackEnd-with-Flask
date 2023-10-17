from app import app, db, response, token_blacklist
from app.model.user import User

from flask import request, jsonify
from flask_jwt_extended import *

import datetime

def data(level, balance):
  try:
    name = request.form.get('name')
    email = request.form.get('email').lower()
    password = request.form.get('password')

    collections = db.collection('users')
    check = collections.where('email', '==', email).get()

    if check:
        return response.badRequest(email, 'That email already use!')
    
    user = User(name=name, email=email, password=password, level=level, id_books=[], balance=balance)
    user.setPassword(password)

    return user
  
  except Exception as e:
    print(e)

# def create_admin():
#   data_json = data(level=1, balance=1000000).to_dict()
#   doc_ref = db.collection('users').document()
#   doc_ref.set(data_json)

#   return response.success(data_json, 'Success add user')

def create_user():
  try:
    data_json = data(level=2, balance=0).to_dict()
    doc_ref = db.collection('users').document()
    doc_ref.set(data_json)

    return response.success(data_json, 'Success add user')
  except AttributeError as e:
    return response.badRequest([], 'That email already use!')

def login():
  try:
    email = request.form.get('email').lower()
    password = request.form.get('password')
    
    collections = db.collection('users')
    user = collections.where('email', '==', email).get()

    if not user:
        return response.badRequest(user, 'Check your email and password!')
    
    data_json = user[0].to_dict()

    name = data_json['name']
    email = data_json['email']
    password_hash = data_json['password']
    level = data_json['level']
    id_books = data_json['id_books']
    balance = data_json['balance']

    user_obj = User(name=name, email=email, password=password_hash, level=level, id_books=id_books, balance=balance)

    if not user_obj.checkPassword(password):
      return response.badRequest([], 'Check your email and password!')

    expires = datetime.timedelta(hours=1)
    expires_refresh = datetime.timedelta(hours=3)

    access_token = create_access_token(data_json, fresh=True, expires_delta=expires)
    refresh_token = create_refresh_token(data_json, expires_delta=expires_refresh)

    dataShow = {
        'data' : data_json,
        'access_token' : access_token,
        'refresh_token' : refresh_token
    }
    
    return dataShow
  
  except Exception as e:
    print(e)

def user_data(id):
  doc_ref = db.collection('users').document(id).get()
  data_json = doc_ref.to_dict()

  name = data_json['name']
  id_books = data_json['id_books']
  balance = data_json['balance']
  level = data_json['level']

  show_data = {
    'name' : name,
    'books' : id_books,
    'balance' : balance,
    'level' : level
  }

  return response.success(show_data, 'Success get user data')

def get_id(email):
  collections = db.collection('users')
  user = collections.where('email', '==', email).get()[0]
  return user.id

def change_password(user, old_jwt_token):

  name = user['name']
  email = user['email']
  password_hash = user['password']
  level = user['level']
  id_books = user['id_books']
  balance = user['balance']

  user_obj = User(name=name, email=email, password=password_hash, level=level, id_books=id_books, balance=balance)

  old_password = request.form.get('oldPassword')
  password = request.form.get('password')
  confirm_password = request.form.get('confirmPassword')

  if password != confirm_password:
    return response.badRequest([], 'Confirm your new password!!!')
  
  if not user_obj.checkPassword(old_password):
    return response.badRequest([], 'Your old password incorrect!!!')
  
  user_obj = User(name=name, email=email, password=password, level=level, id_books=id_books, balance=balance)
  user_obj.setPassword(password)

  user_json = user_obj.to_dict()

  expires = datetime.timedelta(hours=1)
  expires_refresh = datetime.timedelta(hours=3)

  access_token = create_access_token(user_json, fresh=True, expires_delta=expires)
  refresh_token = create_refresh_token(user_json, expires_delta=expires_refresh)

  id_user = get_id(email)

  doc_ref = db.collection('users').document(id_user)
  doc_ref.update(user_json)

  dataShow = {
        'data' : user_json,
        'access_token' : access_token,
        'refresh_token' : refresh_token
    }
  
  token_blacklist.add(old_jwt_token)

  return response.success(dataShow, 'Success change old password!!')
