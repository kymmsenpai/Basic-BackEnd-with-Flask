from app import app, db, response
from app.model.book import Book
from flask import request, jsonify, abort

def allData(docs):
  data = []
  for doc in docs:
    d = doc.to_dict()
    d['id'] = doc.id
    data.append(d)
  return data

def data():
  try:
    title = request.form.get('title')
    author = request.form.get('author')
    genre = request.form.get('genre')
    language = request.form.get('language')
    price = request.form.get('price')
    
    book = Book(title=title, author=author, genre=genre, language=language, price=price)

    return book
  except Exception as e:
    print(e)

def add():
  data_json = data().to_dict()
  doc_ref = db.collection('Books').document()
  doc_ref.set(data_json)
  print('Dokumen berhasil dibuat dengan ID:', doc_ref.id)
  return response.success('', 'Success add book')

def show():
  docs = db.collection('Books').stream()
  data = allData(docs)

  return response.success(data, 'Success see book')

def detail(id):
  try:
    doc_ref = db.collection('Books').document(id)
    doc = doc_ref.get().to_dict()
    if not doc:
      return response.badRequest([], 'Book not found')
    return response.success(doc, 'Success get book what you want')
  except Exception as e:
    print(e)

def change(id):
  try:
    data_json = data().to_dict()
    doc_ref = db.collection('Books').document(id)
    if not doc_ref.get().exists:
      return response.badRequest([], 'Book not found')
    doc_ref.update(data_json)
    return response.success(data_json, 'Success updating book')
  
  except Exception as e:
    print(e)

def delete(id):
  try:
    doc_ref = db.collection('Books').document(id)
    if not doc_ref.get().exists:
      return response.badRequest([], 'Book not found')
    doc_ref.delete()
    return response.success({}, 'Success deleting book')
  
  except Exception as e:
    print(e)