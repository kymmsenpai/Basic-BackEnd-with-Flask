from app import db

class Book():
  def __init__(self, title, author, genre, language, price):
    self.title = str(title)
    self.author = str(author)
    self.genre =  str(genre)
    self.language =  str(language)
    self.price = int(price)
  
  def to_dict(self):
    data = {
      'title' : self.title,
      'author' : self.author,
      'genre' : self.genre,
      'language' : self.language,
      'price' : self.price
    }

    return data