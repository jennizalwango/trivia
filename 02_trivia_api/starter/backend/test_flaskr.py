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
        self.database_path = 'postgres://{}:{}@{}/{}'.format(
            'postgres', 'jenny', '127.0.0.1:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.question = {
            'question': 'question',
            'answer': "okay",
            'category': "1",
            'difficulty': 2
        }
        self.searchData = {
            'searchTerm': 'u'
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

    """TODO Write at least one test for each test for
    successful operation and for expected errors."""

    def test_get_all_categories_sucess(self):

        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['sucess'], True)

    def test_get_all_categories_failure(self):
        response = self.client().get('/categor')
        self.assertEqual(response.status_code, 404)

    def test_failure_to_create_question(self):
        response = self.client().post('/questionss',
                                      content_type='application/json',
                                      data=json.dumps(self.question))

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    def test_successful_question_creation(self):
        response = self.client().post('/questions',
                                      json={'question': 'Sample question?',
                                            'answer': 'Sample answer.',
                                            'difficulty': 2,
                                            'category': '1'})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question successfully created')

    def test_successful_deletion(self):
        res = self.client().post('/questions',
                                 content_type='application/json',
                                 data=json.dumps(self.question))
        response = self.client().delete('/questions/11')
        self.assertEqual(response.status_code, 200)

    def test_failure_to_delete(self):
        res = self.client().post('/questions',
                                 content_type='application/json',
                                 data=json.dumps(self.question))
        response = self.client().delete('/question/j')
        self.assertEqual(response.status_code, 404)

    def test_retrive_questions_by_category_success(self):
        response = self.client().get('categories/1/questions')
        self.assertEqual(response.status_code, 200)

    def test_retrive_questions_by_category_with_wrong_url(self):
        response = self.client().post('/categoriess/0/questions')
        self.assertEqual(response.status_code, 404)

    def test_search_questions(self):
        response = self.client().post('/questions/search',
                                      content_type='application/json',
                                      data=json.dumps(self.searchData))

        self.assertEqual(response.status_code, 200)

    def test_search_with_wrong_url(self):
        sample_data2 = {"search_term": "name"}
        response = self.client().post('/questions/searchs',
                                      content_type='application/json',
                                      data=json.dumps(sample_data2))

        self.assertEqual(response.status_code, 404)

    def test_retrive_questions_sucess(self):
        response = self.client().get('/questions',
                                     content_type='application/json')
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)

    def test_retrive_questions_failure(self):
        response = self.client().patch('/questions')

        self.assertEqual(response.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
