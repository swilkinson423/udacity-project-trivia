import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


# ----------------------------------------------------- #
# --------------------- GLOBAL VARIABLES -------------- #
# ----------------------------------------------------- #

QUESTIONS_PER_PAGE = 10


# ----------------------------------------------------- #
# --------------------- HELPER FUNCTIONS -------------- #
# ----------------------------------------------------- #

def paginate_questions(request, selection):
    # Function returns a selection of questions based on the 
    # number of QUESTIONS_PER_PAGE and the current page.
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def get_categories():
    # Function returns the name of the categories.
    categories = ['null']
    
    for category in Category.query.all():
        categories.append(category.type)
    
    return categories


# ----------------------------------------------------- #
# --------------------- BEGIN APP --------------------- #
# ----------------------------------------------------- #

def create_app(db_URI="", test_config=None):
    app = Flask(__name__)  
    if db_URI:
        print('USING NON-DEFAULT DATABASE')
        setup_db(app,db_URI)
    else:
        print('USING DEFUALT DATABASE')
        setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    @app.route('/questions')
    # Route will return the information to populate the home page,
    # including the categories and paginated selection of questions.
    def retrieve_questions():

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success':True,
            'questions':current_questions,
            'total_questions':len(Question.query.all()),
            'categories': get_categories(),
            'current_category': 0
        })


    @app.route('/categories/<int:category_id>/questions', methods=['GET'] )
    # Route will return the paginated selection of questions for the selected category.
    # TEST: The webpage will display categories and questions
    def get_category_questions(category_id):

        selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success':True,
            'questions': current_questions,
            'total_questions':len(selection),
            'categories': get_categories(),
            'current_category': category_id
        })


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    # Route will delete a question based on the question's ID.
    # TEST: When you click the trash icon next to a question, the question will be removed.
    # TEST: This removal will persist in the database and when you refresh the page.
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            category_id = question.category

            if question is None:
                abort(404)
            
            question.delete()
            
            selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions':len(selection),
                'categories': get_categories(),
                'current_category': category_id
            })
        except:
            abort(422)

    @app.route('')
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

