from app import app, response
from app import token_blacklist
from app.controller import bookController, userController, userbookController, apiController

from flask import request, redirect, url_for, render_template, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required

from firebase_admin import auth
from datetime import datetime, timedelta


@app.route('/')
def index():
  return 'Just imagine this is a login page :\')'

@app.route('/books', methods=['GET', 'POST'])
@jwt_required()
def books():
  user = get_jwt_identity()
  level = user['level']
  if request.method == 'GET':
    return bookController.show()
  else:
    if level == 1:
      return bookController.add()
    else:
      return response.badRequest([], "You're not admin")
  
@app.route('/books/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def book_detail(id):
  user = get_jwt_identity()
  level = user['level']
  if request.method == 'GET':
      return bookController.detail(id)
  
  if level == 1:
    if request.method == 'PUT':
      return bookController.change(id)
    elif request.method == 'DELETE':
      return bookController.delete(id)
  else:
    return response.badRequest([], "You're not admin")

# @app.route('/create-admin', methods=['POST'])
# def admins():
#   return userController.create_admin()

@app.route('/create-user', methods=['POST'])
def users():
  return userController.create_user()

@app.route('/login', methods=['POST'])
def logins():
  return userController.login()
  # jwt_token = data_user['access_token']
  # response = redirect(f'/protected')
  # response.headers['Authorization'] = f"Bearer {jwt_token}"
  # return response

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    user_id = userController.get_id(current_user['email'])
    return redirect(f'/user/{user_id}')

@app.route('/user/<id>', methods=['GET'])
@jwt_required()
def user_login(id):
  current_user = get_jwt_identity()
  user_id = userController.get_id(current_user['email'])
  if id == user_id:
    return userController.user_data(user_id)
  return redirect('/protected')

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return redirect('/')

@app.route('/buy/<id_book>', methods=['POST'])
@jwt_required()
def buy_book(id_book):
  current_user = get_jwt_identity()
  user_id = userController.get_id(current_user['email'])
  return userbookController.buy(id_book, user_id)

@app.route('/user/collections', methods=['GET'])
@jwt_required()
def user_collections():
  current_user = get_jwt_identity()
  user_id = userController.get_id(current_user['email'])
  return userbookController.all_user_books(user_id)

@app.route('/api/v1/books', methods=['GET'])
def api_books():
  return apiController.books()

@app.route('/user/change-password', methods=['PUT'])
@jwt_required()
def change_password():
  jwt_token = request.headers.get('Authorization').split(' ')[1]
  if jwt_token in token_blacklist:
    return response.badRequest([], 'Please login again!!!')
  user = get_jwt_identity()
  return userController.change_password(user, jwt_token)