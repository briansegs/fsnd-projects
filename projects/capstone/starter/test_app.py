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

        self.new_actor = {
            'name': 'Sam England',
            'age': '25',
            'gender': 'male'
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

    # def test_405_invalid_method(self):
    #     res = self.client().patch('/categories')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Method Not Allowed')

    # def test_get_paginated_questions(self):
    #     res = self.client().get('/questions/')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertEqual(data['current_category'], None)
    #     self.assertTrue(data['categories'])

    # def test_404_sent_requesting_beyond_valid_page(self):
    #     res = self.client().get('/questions/?page=1001')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Resource Not Found')

    # def test_delete_question(self):
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)

    #     created_id = data['created']

    #     res = self.client().delete('/questions/' + str(created_id))
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 1).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], created_id)
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(len(data['questions']))
    #     self.assertEqual(question, None)

    # def test_422_if_question_does_not_exist(self):
    #     res = self.client().delete('/questions/2002')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Unprocessable Entity')

    # def test_creat_new_question(self):
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])

    # def test_400_if_bad_request(self):
    #     res = self.client().post('/questions', json=self.new_bad_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Bad Request')

    # def test_get_question_by_search(self):
    #     res = self.client().post('/questions/search/', json=self.search_term)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertEqual(data['current_category'], None)
    #     self.assertTrue(data['categories'])

    # def test_404_if_resource_not_found(self):
    #     res = self.client().post('/questions/search/', json=self.bad_search)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Resource Not Found')

    # def test_get_question_by_category(self):
    #     res = self.client().get('/categories/2/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertEqual(data['current_category'], None)
    #     self.assertTrue(data['categories'])

    # def test_category_405_if_invalid_method(self):
    #     res = self.client().delete('/categories/1001/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Invalid Method')

    # def test_get_quizz_questions(self):
    #     res = self.client().post('/quizzes', json=self.category)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['question'])

    # def test_quizzes_405_if_invalid_method(self):
    #     res = self.client().get('/quizzes', json=self.category)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Invalid Method')


if __name__ == "__main__":
    unittest.main()
