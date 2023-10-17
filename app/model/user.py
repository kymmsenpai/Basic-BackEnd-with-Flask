from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User():
    def __init__(self, name, email, password, level, id_books, balance):
      self.name = str(name)
      self.email = str(email)
      self.password = str(password)
      self.level = int(level)
      self.id_books = []
      self.balance = int(balance)
      self.created_at = datetime.utcnow()
      self.updated_at = datetime.utcnow()
    
    def to_dict(self):
       data = {
          'name' : self.name,
          'email' : self.email,
          'password' : self.password,
          'level' : self.level,
          'id_books' : self.id_books,
          'balance' : self.balance,
          'created_at' : self.created_at,
          'updated_at' : self. updated_at
       }

       return data
    
    def setPassword(self, password):
        self.password = generate_password_hash(password)
    
    def checkPassword(self, password):
        return check_password_hash(self.password, password)
    
    