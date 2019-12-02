import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(page, selections):
  page = request.args.get('page', 1, type=int)
  start = [page -1] * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  allSelected = []
  for  Qnts, category in selections:
    Qnts = Qnts.format()
    Qnts['category_id'] = Qnts['category']
    Qnts['categroy'] = categroy
    allSelected.append(Qnts)

  current_questions = allSelected[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/*":{"origins":"*"}})
  
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
    }), 200


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

  @app.route('/question')
  def retrive_questions():

    page = request.args.get('page', 1, type=int)

    questions = Question.query.join(
      Category,
      Category.id == Question.category
    ).add_columns(Category.type).all()

    current_questions = paginate_questions(page, questions)

    categories = []
    results = Category.query.all()
    for  result in results:
      categories.append(result.type)

    if len(current_questions) ==0:
      abort(404, "Sorry no question found")

    return jsonify({
      'sucess': True,
      'questions': current_questions,
      'total_questions':len(questions),
      'catgry': categories,
      'current_category': "all"
    }), 200



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/question/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

      question = Question.query_by(Question.id == question_id).one_or_none()

      if question is none:
        abort(404, 'sorry question not found')
        question.delete()

        selection = Question.query.order_by(Question.id).all()
        current_questions= paginate_questions(page, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'message': 'Question have benn sucessfully deleted',
        'total_questions': len(Question.query.all())
      })


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    data = request.get_json()

    question = data.get('question', None)
    category = data.get('categroy', None)
    answer = int(data.get('answer', None))
    difficulty = int(data.get('difficulty', None))

    question = Question(
      answer=answer, 
      category=category, 
      question=question, 
      difficulty=difficulty
      )
    
    is_valid = validator.question(question)
    if not (is_valid is True):
      abort(400, is_valid)

    question.insert()
    return jsonify({
      'success': True,
      'created': question_id,
      'meassge':'Question successfully created'
    }), 201

      
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/question/search', methods=['POST'])
  def question_search():
    data = request.get_json()
    new_search = data.get('new_search', None)

    page = request.args.get('page', 1, type=int)

    questions = Question.query.join(
      Category, Category.id == Question.category
    ).add_columns(Category.type).all()

    current_questions = paginate_questions(page, questions)
    
    question_list = []
    for qn in current_questions:
      if new_search.lower() in question['question'].lower():
        question_list.append(questions)


    categories = []
    results = Category.query.all()
    for result in  results:
      categories.append(result.type)
    
    return jsonify({
      'sucess': True,
      'questions': questions,
      'total_questions': len(questions),
      'categories':categories,
      'Avaliabe_category':None
    }), 200

    
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def retrive_question_by_category(category_id):

    questions = Question.query.order_by(category_id=Category.id).join(
      Category,
      Category.id == Question.category
    ).add_columns(Category.type).all()

    current_questions = paginate_questions(page, questions)

    if len(current_questions) == 0:
      abort(404, 'Not found.')
    
    category = Category.query.filter_by(category_id=Category.id).first()
    categories = []

    results = Category.query.all()
    for result in results:
      categories.append(result.type)
    
    return jsonify({
      'sucess': True,
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': categories,
      'Avaliable_category': category.type
    }), 200


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
  @app.route('/quiz', methods=['POST'])
  def create_quiz():

    data  = request.get_json()

    questions = Question.query.filter_by(
      categroy=data.get('quiz_category')['id']
    ).filter(Question.id.notin__(data.get('previous_questions'))).all()

    if data.get('quiz_category')['id'] == 0:
      questions = Question.query.filter(
        Question.id.notin_(data.get('previous_questions'))
      ).all()

      question = None
      if questions:
        question = random.choice(questions).format()

      return jsonify({
        'sucess': True,
        'question':question
      }), 200

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success':False,
      'error': 404,
      'message': 'response not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'sucess':False,
      'error': 400,
      'message': 'its bad request'
    }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'sucess': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405
 
  return app

    