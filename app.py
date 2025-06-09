from flask import Flask, render_template, request, redirect, url_for, abort
from sqlalchemy.orm import joinedload

from datamanager.sqlite_data_manager import SQLiteDataManager, User, Movie, Review

# ─── Flask-App und DataManager ────────────────────────────────────────────────

app = Flask(__name__)

# Standard-Datenbank (für Tests überschreibbar via app.data_manager = ...)
app.data_manager = SQLiteDataManager('moviwebapp.db')
dm = app.data_manager

# ─── Web-Seiten ────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    users = dm.get_all_users()
    return render_template('users.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    if not name:
        return "Missing name", 400
    user = User(name=name)
    dm.add_user(user)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = dm.get_user_by_id(user_id)
    if not user:
        abort(404, description="User not found")

    movies = dm.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    user = dm.get_user_by_id(user_id)
    if not user:
        abort(404, description="User not found")

    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year', type=int)  # optional
        if not title:
            return "Missing title", 400
        movie = Movie(title=title, year=year, user_id=user_id)
        dm.add_movie(movie)
        return redirect(url_for('user_movies', user_id=user_id))

    # GET: Formular anzeigen
    return render_template('add_movie.html', user=user)


@app.route('/movies/<int:movie_id>/reviews', methods=['GET', 'POST'])
def movie_reviews(movie_id):
    movie = dm.get_movie_by_id(movie_id)
    if not movie:
        abort(404, description="Movie not found")

    users = dm.get_all_users()

    if request.method == 'POST':
        user_id = request.form.get('user_id', type=int)
        review_text = request.form.get('review_text')
        rating = request.form.get('rating', type=int)
        if not (user_id and review_text and rating):
            return "Missing fields", 400

        review = Review(user_id=user_id, movie_id=movie_id, text=review_text, rating=rating)
        dm.add_review(review)
        return redirect(url_for('movie_reviews', movie_id=movie_id))

    # GET: Reviews abfragen (eager load, damit review.user.name funktioniert)
    reviews = dm.get_reviews_for_movie(movie_id)  # falls nötig: implementiere .options(joinedload(Review.user))
    return render_template('movie_reviews.html', movie=movie, reviews=reviews, users=users)


if __name__ == '__main__':
    app.run(debug=True)
