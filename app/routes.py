from flask import redirect, render_template, request, url_for
from app import app, db
from app.forms import AuthorForm, MovieForm
from app.models import Author, Movie


def sort_movies(movies_list, sort_by):
    if sort_by:
        movies_list.sort(key=lambda movie: getattr(movie, sort_by))

@app.route("/movies/", methods=["GET", "POST"])
def movies_list():
    movie_form = MovieForm()
    author_form = AuthorForm()
    error = ""
    if request.method == "POST":
        if movie_form.validate_on_submit():
            movie = Movie(title=movie_form.data['title'],
                           year=movie_form.data['year'],
                           authors=movie_form.data['authors'])  
            db.session.add(movie)
            db.session.commit()
        return redirect(url_for("movies_list"))
    sort_by = request.args.get('sort_by')
    movies = Movie.query.all()
    authors = Author.query.all()
    sort_movies(movies, sort_by)
    return render_template("movies.html", movie_form=movie_form, author_form=author_form, movies=movies, authors=authors, error=error)

@app.route("/add_author/", methods=["POST"])
def add_author():
    form = AuthorForm()
    error = ""
    if not form.validate_on_submit():
        return redirect(url_for("movies_list", error=error))
    author = Author(name=form.data['name'])
    db.session.add(author)
    db.session.commit()
    return redirect(url_for("movies_list"))



@app.route("/movies/<int:movie_id>/", methods=["GET", "POST"])
def movie_details(movie_id):
    movie = movies.get(movie_id - 1)
    form = MovieForm(data=movie)

    if request.method == "POST":
        if form.validate_on_submit():
            movies.update(movie_id - 1, form.data)
        return redirect(url_for("movies_list"))
    return render_template("movie.html", form=form, movie_id=movie_id)
