from flask import redirect, render_template, request, url_for
from sqlalchemy import func
from app import app, db
from app.forms import AuthorForm, MovieForm, RentForm
from app.models import Author, Movie, MovieRent


def sort_movies(movies_list, sort_by):
    if sort_by:
        movies_list.sort(key=lambda movie: getattr(movie, sort_by))

@app.route("/movies/", methods=["GET", "POST"])
def movies_list():
    movie_form = MovieForm()
    author_form = AuthorForm()
    rent_form = RentForm()
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
    movie_query = Movie.query.join(MovieRent, Movie.id == MovieRent.movie_id, isouter=True)
    movies = movie_query.all()
    authors = Author.query.all()
    sort_movies(movies, sort_by)
    return render_template("movies.html", movie_form=movie_form, author_form=author_form, rent_form=rent_form, movies=movies, authors=authors, error=error)

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

@app.route("/rent_movie/<int:movie_id>/", methods=["POST"])
def rent_movie(movie_id):
    error = ""
    active_rent = (MovieRent
        .query
        .filter(MovieRent.movie_id==movie_id)
        .filter(MovieRent.end == None)
    ).first()

    if not active_rent:
        new_rent = MovieRent(movie_id=movie_id, start=func.now(), end=None)
        db.session.add(new_rent)
    else:
        active_rent.end = func.now()

    db.session.commit()

    return redirect(url_for("movies_list"))

@app.route("/movies/<int:movie_id>/", methods=["GET", "POST"])
def movie_details(movie_id):
    movie = Movie.query.filter(Movie.id==movie_id).first_or_404()
    form = MovieForm(obj=movie)

    if request.method == "POST":
        if form.validate_on_submit():
            movie.title = form.data['title']
            movie.year = form.data['year']
            db.session.commit()
        return redirect(url_for("movies_list"))
    return render_template("movie.html", form=form, movie_id=movie_id)

@app.route("/authors/<int:author_id>/", methods=["GET", "POST"])
def author_details(author_id):
    author = Author.query.filter(Author.id==author_id).first_or_404()
    form = AuthorForm(obj=author)

    if request.method == "POST":
        if form.validate_on_submit():
            author.name = form.data['name']
            db.session.commit()
        return redirect(url_for("movies_list"))
    return render_template("author.html", form=form, author_id=author_id)
