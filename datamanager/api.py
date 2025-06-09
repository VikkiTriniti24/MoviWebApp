# datamanager/api.py

from flask import Blueprint, jsonify, request
from datamanager.sqlite_data_manager import SQLiteDataManager, User

api = Blueprint('api', __name__)
# DataManager-Instanz (kein Parameter nötig)
dm = SQLiteDataManager()

@api.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        all_users = dm.get_all_users()
        return jsonify([{'id': u.id, 'name': u.name} for u in all_users])

    # POST: neuen User anlegen
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing name field'}), 400
    user = User(name=data['name'])
    dm.add_user(user)
    return jsonify({'id': user.id, 'name': user.name}), 201

@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = dm.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name})

@api.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    user = dm.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'GET':
        movies = dm.get_user_movies(user_id)
        return jsonify([{'id': m.id, 'title': m.title, 'year': m.year} for m in movies])

    # POST: neuen Film hinzufügen
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Missing movie title'}), 400
    title = data['title']
    year = data.get('year')  # optional
    movie_id = dm.add_movie_to_user(user_id, title, year)
    return jsonify({'message': 'Movie added', 'movie_id': movie_id}), 201

@api.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = dm.get_movie_by_id(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'year': movie.year,
        'user_id': movie.user_id
    })

@api.route('/movies/<int:movie_id>/reviews', methods=['GET', 'POST'])
def movie_reviews(movie_id):
    # GET: alle Reviews
    movie = dm.get_movie_by_id(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    if request.method == 'GET':
        reviews = dm.get_reviews_for_movie(movie_id)
        return jsonify([
            {'user_id': r.user_id, 'text': r.text, 'rating': r.rating}
            for r in reviews
        ])

    # POST: neue Review anlegen
    data = request.get_json()
    if not data or not all(k in data for k in ('user_id', 'text', 'rating')):
        return jsonify({'error': 'Missing review fields'}), 400
    review = dm.add_review_from_data(
        data['user_id'], movie_id, data['text'], data['rating']
    )
    return jsonify({'message': 'Review added', 'review_id': review.id}), 201


