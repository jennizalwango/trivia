import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgres://{}:{}@{}/{}'.format('postgres', 'jenny', '127.0.0.1:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.question = {
            'question':'question',
            'answer': 8,
            'category': 1,
            'difficulty':2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories_sucess(self):

        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['sucess'], True)


    def test_get_all_categories_with_wrong_url(self):
        response = self.client().get('/categor')
        self.assertEqual(response.status_code, 404)

    def test_failure_to_create_question(self):
        response = self.client().post('/questionss', content_type='application/json', data=json.dumps(self.question))

        data= json.loads(response.data)
        self.assertEqual(response.status_code, 404)


    def test_successful_question_creation(self):
        response = self.client().post('/questions', content_type='application/json', data=json.dumps(self.question))

        data= json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['meassge'], 'Question successfully created')

    def test_successful_deletion(self):
        res = self.client().post('/questions', content_type='application/json', data=json.dumps(self.question))
        response = self.client().delete('/question/2')
        self.assertEqual(response.status_code, 200)

    def test_failure_to_delete(self):
        res = self.client().post('/questions', content_type='application/json', data=json.dumps(self.question))
        response = self.client().delete('/question/j')
        self.assertEqual(response.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()