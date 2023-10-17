from app import app, db, response

def buy(id_book, id_user):
  book_ref = db.collection('Books').document(id_book)
  book_json = book_ref.get().to_dict()
  price = book_json['price']

  user_ref = db.collection('users').document(id_user)
  user_json = user_ref.get().to_dict()
  balance = user_json['balance']
  user_book = user_json['id_books']

  if balance >= price:
    user_book.append(id_book)
    balance -= price

    user_ref.update({
      'balance': balance,
      'id_books': user_book
    })

    return response.success(book_json, "Success buy a Book")
  else:
    return response.badRequest([], "Balance not enough")

def all_user_books(id):
  doc_ref = db.collection('users').document(id)
  user_json = doc_ref.get().to_dict()

  data_books = []

  id_books = user_json['id_books']

  for id_book in id_books:
    doc_ref = db.collection('Books').document(id_book)
    book_json = doc_ref.get().to_dict()
    del book_json['price']
    data_books.append(book_json)

  if data_books == []:
    return response.success([], "Buy a book first")
  return response.success(data_books, "Success")
  