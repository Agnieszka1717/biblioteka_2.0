from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class MovieForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    year = IntegerField('year', validators=[DataRequired()])

class AuthorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])