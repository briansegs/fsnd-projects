import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actor, Movie


def create_app(test_congig=None):
	app = Flask(__name__)
	CORS(app)
	setup_db(app)
	db_drop_and_create_all()

	@app.route('/')
	def health():
		return jsonify("Healthy")

	@app.route('/movies')
	def get_movies():
		movie_list = Movie.query.all()
		if movie_list is None:
			abort(404)

		movies = [movie.format() for movie in movie_list]

		return jsonify({
			"success": True,
			"movies": movies
		}), 200

	@app.route('/actors')
	def get_actors():
		actor_list = Actor.query.all()
		if actor_list is None:
			abort(404)

		actors = [actor.format() for actor in actor_list]

		return jsonify({
			"success": True,
			"actors": actors
		}), 200

	@app.route('/movies/<movie_id>', methods=['DELETE'])
	def delete_movie(movie_id):
		try:
			movie = (
				Movie.query.filter(Movie.id == movie_id).one_or_none()
			)

			if movie is None:
				abort(404)

			movie.delete()

			return jsonify({
				"success": True,
				"delete": movie_id
			}), 200

		except Exception:
			abort(422)

	@app.route('/actors/<actor_id>', methods=['DELETE'])
	def delete_actor(actor_id):
		try:
			actor = (
				Actor.query.filter(Actor.id == actor_id).one_or_none()
			)

			if actor is None:
				abort(404)

			actor.delete()

			return jsonify({
				"success": True,
				"delete": actor_id
			}), 200

		except Exception:
			abort(422)

	return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)




