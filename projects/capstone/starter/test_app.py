import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db_drop_and_create_all, setup_db, Actor, Movie
from tokens import assistant_token, director_token, producer_token


class TestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'admin', 'localhost:5432', self.database_name
            )

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            db_drop_and_create_all()


        self.assistant_jwt = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(assistant_token)
            }

        self.director_jwt = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(director_token)
            }

        self.producer_jwt = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(producer_token)
            }

        self.new_movie = {
            'title': 'Head Strong',
            'release_date': '2020'
        }

        self.new_bad_movie = {
            'title': '',
            'release_date': ''
        }

        self.new_actor = {
            'name': 'Sam England',
            'age': '25',
            'gender': 'male'
        }

        self.new_bad_actor = {
            'name': ''
        }

        self.new_title = {
            'title': 'Iron Mind',
        }

        self.new_name = {
            'name': 'Sammy E',
        }


    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_health(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Healthy")

    #Assistant

    def test_assistant_get_movies(self):
        res = self.client().get('/movies', headers=self.assistant_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['movies']), list)

    def test_assistent_get_actors(self):
        res = self.client().get('/actors', headers=self.assistant_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['actors']), list)

    def test_assistent_post_movie(self):
        res = self.client().post('/movies', headers=self.assistant_jwt, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found.')

    def test_assistent_post_actor(self):
        res = self.client().post('/actors', headers=self.assistant_jwt, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found.')

    def test_assistent_patch_movie(self):
        res = self.client().patch('/movies/1', headers=self.assistant_jwt, json=self.new_title)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found.')

    def test_assistent_patch_actor(self):
        res = self.client().patch('/actors/1', headers=self.assistant_jwt, json=self.new_name)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found.')

    def test_assistent_delete_movie(self):
        res = self.client().delete('/movies/1', headers=self.assistant_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found.')

    def test_assistent_delete_actor(self):
        res = self.client().delete('/actors/1', headers=self.assistant_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found.')

    #Director

    def test_director_get_movies(self):
        res = self.client().get('/movies', headers=self.director_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['movies']), list)

    def test_director_get_actors(self):
        res = self.client().get('/actors', headers=self.director_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['actors']), list)

    def test_director_post_movie(self):
        res = self.client().post('/movies', headers=self.director_jwt, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found.')

    def test_director_post_actor(self):
        res = self.client().post('/actors', headers=self.director_jwt, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_director_patch_movie(self):
        res = self.client().post('/movies', headers=self.producer_jwt, json=self.new_movie)
        data = json.loads(res.data)

        res = self.client().patch('/movies/1', headers=self.director_jwt, json=self.new_title)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_director_patch_actor(self):
        res = self.client().post('/actors', headers=self.director_jwt, json=self.new_actor)
        data = json.loads(res.data)

        res = self.client().patch('/actors/1', headers=self.director_jwt, json=self.new_name)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_director_delete_movie(self):
        res = self.client().delete('/movies/1', headers=self.director_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found.')

    def test_director_delete_actor(self):
        res = self.client().post('/actors', headers=self.director_jwt, json=self.new_actor)
        data = json.loads(res.data)

        res = self.client().delete('/actors/1', headers=self.director_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])

    #Producer

    def test_producer_get_movies(self):
        res = self.client().get('/movies', headers=self.producer_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['movies']), list)

    def test_producer_get_actors(self):
        res = self.client().get('/actors', headers=self.producer_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['actors']), list)

    def test_producer_post_movie(self):
        res = self.client().post('/movies', headers=self.producer_jwt, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_producer_post_actor(self):
        res = self.client().post('/actors', headers=self.producer_jwt, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_producer_patch_movie(self):
        res = self.client().post('/movies', headers=self.producer_jwt, json=self.new_movie)
        data = json.loads(res.data)

        res = self.client().patch('/movies/1', headers=self.producer_jwt, json=self.new_title)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_producer_patch_actor(self):
        res = self.client().post('/actors', headers=self.producer_jwt, json=self.new_actor)
        data = json.loads(res.data)

        res = self.client().patch('/actors/1', headers=self.producer_jwt, json=self.new_name)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_producer_delete_movie(self):
        res = self.client().post('/movies', headers=self.producer_jwt, json=self.new_movie)
        data = json.loads(res.data)

        res = self.client().delete('/movies/1', headers=self.producer_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])

    def test_producer_delete_actor(self):
        res = self.client().post('/actors', headers=self.producer_jwt, json=self.new_actor)
        data = json.loads(res.data)

        res = self.client().delete('/actors/1', headers=self.producer_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])

    #Error behavior of endpoints

    def test_movies_405_invalid_method(self):
        res = self.client().patch('/movies', headers=self.assistant_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Method Not Allowed')

    def test_actors_405_invalid_method(self):
        res = self.client().patch('/actors', headers=self.assistant_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Method Not Allowed')

    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1', headers=self.producer_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')

    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1', headers=self.producer_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')

    def test_movie_400_if_bad_request(self):
        res = self.client().post('/movies',headers=self.producer_jwt, json=self.new_bad_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Bad Request')

    def test_actor_400_if_bad_request(self):
        res = self.client().post('/actors',headers=self.producer_jwt, json=self.new_bad_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Bad Request')

    def test_movie_422_if_movie_is_none(self):
        res = self.client().patch('/movies/100', headers=self.producer_jwt, json=self.new_title)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')

    def test_movie_422_if_actor_is_none(self):
        res = self.client().patch('/actors/100', headers=self.producer_jwt, json=self.new_name)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')


if __name__ == "__main__":
    unittest.main()
