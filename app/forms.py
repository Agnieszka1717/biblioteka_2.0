from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, SubmitField
from wtforms_sqlalchemy.orm import QuerySelectMultipleField
from wtforms.validators import DataRequired

from app.models import Author, Movie
from app import app

def all_authors():
    with app.app_context():
        return Author.query.all()

class MovieForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    year = IntegerField('year', validators=[DataRequired()])
    authors = QuerySelectMultipleField('authors', query_factory=all_authors, get_label="name", validators=[DataRequired()])

class AuthorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

class RentForm(FlaskForm):
    submit_field = SubmitField('Go', validators=[DataRequired()])