from app import app, db, response
from flask import request, jsonify

def allData(docs):
  data = []
  for doc in docs:
    d = doc.to_dict()
    data.append(d)
  return data

def genre(genre=None):
  coll = db.collection('Books')
  if genre != None and genre != "":
    genre_book = coll.where('genre', '==', genre).get()
    return [gb.to_dict() for gb in genre_book]
  docs = db.collection('Books').stream()
  all_genre = allData(docs)
  return all_genre

def author(author=None):
  coll = db.collection('Books')
  if author != None and author != "":
    author_book = coll.where('author', '==', author).get()
    return [ab.to_dict() for ab in author_book]
  docs = db.collection('Books').stream()
  all_author = allData(docs)
  return all_author

def language(language=None):
  coll = db.collection('Books')
  if language != None and language != "":
    language_book = coll.where('language', '==', language).get()
    return [lb.to_dict() for lb in language_book]
  docs = db.collection('Books').stream()
  all_language = allData(docs)
  return all_language

def books():
  genre_book = request.args.get('genre')
  author_book = request.args.get('author')
  language_book = request.args.get('language')

  list_genre = genre(genre_book)
  list_author = author(author_book)
  list_language = language(language_book)

  filtered = [book for book in list_genre if book in list_author and book in list_language]

  if filtered != []:
    return response.success(filtered, "Success find data")
  else:
    return response.success(filtered, "Data not found")
  

