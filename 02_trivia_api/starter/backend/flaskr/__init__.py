import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1 type=int)
  start = [page -1] * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-control-Allow-Headers', "content-Type, Authorization")
    response.headers.add('Acsess-control-Allow-Methods', 'GET , POST, PATCH, DELETE, OPTIONS')
    return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    orgnised_categories = [categories.format() for category in categories]
    return jsonify({
      'sucess': True,
      'cates':orgnised_categories
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def retrive_questions():
      question = Question.query.order_by(Question.id).all()
      formatted_questions =  paginate_questions(request, selection)
      # formatted_questions = [questions.format() for question in questions]

    if len(formatted_questions) == 0:
      abort 404

    return jsonify({
      'sucess': True,
      'cates':formatted_questions
      'total_questions': len(Question.query.all())
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=[DELETE])
  def delete_question(question_id):
    try:
      question = Question.query_by(Question.id == question.id).one_or_none()
      if question is none:
        abort(404)
        question.delete()
        selection = Question.query.order_by(Question.id).all()
        formatted_questions= paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'deleted': question_id,
          'total_questions': len(Question.query.all())
        })
    except:
      abort(422)

  


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/question', methods['POST'])
  def create_question():
    data = request.get_json()
    new_question = data.get('question', None)
    category = data.get('categroy', None)
    answer_text = data.get('answer_text', None)

    try:
      question = Question(answer_text=answer_text, category=category, new_question=new_question)
      question.insert()
      selection = Question.query.order_by(Question.id).all()
      formatted_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created': question_id,
        'questions':formatted_questions,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)



  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/question', methods['POST'])
  def create_question():
    data = request.get_json()
    new_search = data.get('new_search', None)
    try:
      selection = Question.query.order_by(Question.id).all()
      formatted_questions = paginate_questions(request, selection)
      return jsonify({
        'sucess': True,
        'created':question_id,
        'questions': formatted_questions,
        'total_questions':len(Question.query.all())
      })

    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
@app.route('/quiz', methods['POST'])
def create_quiz():
  data  = request.get_json()

  new_category = data.get('category', None)
  previous_questions = data.get('previous_questions', None)

  try:
    created_quiz = Question(category=new_category,previous_questions=previous_questions)
    created_quiz.insert()
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    