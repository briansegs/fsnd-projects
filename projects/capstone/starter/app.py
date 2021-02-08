import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth


def create_app(test_congig=None):
	app = Flask(__name__)
	CORS(app)
	setup_db(app)
	db_drop_and_create_all()

	# ROUTES

	@app.route('/')
	def health():
		return jsonify({
      		"success": True,
        	"message": "Healthy"
      	}), 200

	@app.route('/movies')
	@requires_auth('get:movies')
	def get_movies(jwt):
		movie_list = Movie.query.order_by(Movie.id).all()
		if movie_list is None:
			abort(404)

		movies = [movie.format() for movie in movie_list]

		return jsonify({
			"success": True,
			"movies": movies
		}), 200

	@app.route('/actors')
	@requires_auth('get:actors')
	def get_actors(jwt):
		actor_list = Actor.query.order_by(Actor.id).all()
		if actor_list is None:
			abort(404)

		actors = [actor.format() for actor in actor_list]

		return jsonify({
			"success": True,
			"actors": actors
		}), 200

	@app.route('/movies/<movie_id>', methods=['DELETE'])
	@requires_auth('delete:movie')
	def delete_movie(jwt, movie_id):
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
	@requires_auth('delete:actor')
	def delete_actor(jwt, actor_id):
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

	@app.route('/movies', methods=['POST'])
	@requires_auth('post:movie')
	def create_movie(jwt):
		body = request.get_json()

		new_title = body.get('title')
		new_release_date = body.get('release_date')

		movie = Movie(
				title=new_title,
				release_date=new_release_date
			)
		try:
			movie.insert()
			return jsonify({
				'success': True,
				'movie': movie.format()
			}), 200

		except Exception:
			abort(422)

	@app.route('/actors', methods=['POST'])
	@requires_auth('post:actor')
	def create_actor(jwt):
		body = request.get_json()

		new_name = body.get('name')
		new_age = body.get('age')
		new_gender = body.get('gender')

		actor = Actor(
				name=new_name,
				age=new_age,
				gender=new_gender
			)
		try:
			actor.insert()
			return jsonify({
				'success': True,
				'actor': actor.format()
			}), 200

		except Exception:
			abort(422)

	@app.route('/movies/<movie_id>', methods=['PATCH'])
	@requires_auth('patch:movie')
	def patch_movie(jwt, movie_id):
		body = request.get_json()

		try:
			movie = (
				Movie.query.filter(Movie.id == movie_id).one_or_none()
				)
			if movie is None:
				abort(404)

			new_title = body.get('title')
			new_release_date = body.get('release_date')

			if new_title is not None:
				movie.title = new_title
			if new_release_date is not None:
				movie.release_date = new_release_date

			movie.update()

			return jsonify({
				'success': True,
				'movie': movie.format()
				}), 200

		except Exception:
			abort(422)


	@app.route('/actors/<actor_id>', methods=['PATCH'])
	@requires_auth('post:actor')
	def patch_actor(jwt, actor_id):
		body = request.get_json()

		try:
			actor = (
				Actor.query.filter(Actor.id == actor_id).one_or_none()
				)
			if actor is None:
				abort(404)

			new_name = body.get('name')
			new_age = body.get('age')
			new_gender = body.get('gender')

			if new_name is not None:
				actor.name = new_name
			if new_age is not None:
				actor.age = new_age
			if new_gender is not None:
				actor.gender = new_gender

			actor.update()

			return jsonify({
				'success': True,
				'actor': actor.format()
				}), 200

		except Exception:
			abort(422)

	# Error Handling


	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
			'success': False,
			'error': 404,
			'message': 'Resource Not Found'
        }), 404

	@app.errorhandler(405)
	def not_allowed(error):
		return jsonify({
			'success': False,
			'error': 405,
			'message': 'Method Not Allowed'
        }), 405

	@app.errorhandler(422)
	def unprocessable_entity(error):
		return jsonify({
			'success': False,
			'error': 422,
			'message': 'Unprocessable Entity'
        }), 422

	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({
			'success': False,
			'error': 400,
			'message': 'Bad Request'
        }), 400


	return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)




