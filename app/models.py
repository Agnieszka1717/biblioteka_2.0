from app import db

class Movie(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(300), index=True)
   year = db.Column(db.Integer)

class Author(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(300), index=True)

class MovieAuthor(db.Model):
   author_id = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key=True)
   movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
