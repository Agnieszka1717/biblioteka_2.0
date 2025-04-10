from app import db

movie_author = db.Table(
    "movie_author",
    db.Column("author_id", db.Integer, db.ForeignKey('author.id'), primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey('movie.id'), primary_key=True),
)

class Movie(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(300), index=True)
   year = db.Column(db.Integer)
   authors = db.relationship("Author", secondary="movie_author", back_populates="movies")
   rents = db.relationship("MovieRent", back_populates="movies")

class Author(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(300), index=True)
   movies = db.relationship("Movie", secondary="movie_author", back_populates="authors")

class MovieRent(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
   start = db.Column(db.DateTime, nullable=False)
   end = db.Column(db.DateTime)
   movies = db.relationship("Movie",back_populates="rents")
