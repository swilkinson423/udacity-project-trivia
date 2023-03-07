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

    # ----------------------------------------------------- #
    # --------------------- ENDPOINTS --------------------- #
    # ----------------------------------------------------- #

    @app.route('/questions', methods=['GET'])
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
            'total_questions':len(selection),
            'categories': get_categories(),
            'current_category': 0
        })


    @app.route('/categories', methods=['GET'])
    # Route will return list of categories.
    def retrieve_categories():

        return jsonify({
            'success':True,
            'categories': get_categories()
        })


    @app.route('/categories/<int:category_id>/questions', methods=['GET'] )
    # Route will return the paginated selection of questions for the selected category.
    def get_category_questions(category_id):

        selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success':True,
            'questions': current_questions,
            'total_questions':len(selection),
            'categories': get_categories(),
            'current_category': category_id
        })


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    # Route will delete a question based on the question's ID.
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


    @app.route('/questions', methods=['POST'])
    # Route for posting a new question. 
    def post_question():

        body = request.get_json()

        new_question    = body.get("question", None)
        new_answer      = body.get("answer", None)
        new_difficulty  = body.get("difficulty", None)
        new_category    = body.get("category", None)

        if new_question & new_answer & new_difficulty & new_category:

            try: 
                question = Question(
                    question    = new_question,
                    answer      = new_answer,
                    difficulty  = new_difficulty,
                    category    = new_category
                )

                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions':len(selection),
                    'categories': get_categories(),
                    'current_category': 0
                })

            except:
                abort(422)
        else:
            abort(400)


    @app.route('/questions/search', methods=['POST'])
    # Route returns questions based on search term.
    def search_questions():

        body = request.get_json()

        try:
            search_term = body.get('searchTerm',None)

            selection = Question.query.filter(Question.question.ilike(r"%{}%".format(search_term))).order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions':len(selection),
                'categories': get_categories(),
                'current_category': 0
            })

        except:
            abort(400)


    @app.route('/quizzes', methods=['POST'])
    # Route for getting questions to play the quiz.
    def play_quiz():

        body = request.get_json()

        category            = body.get('quiz_category', None)['id']
        previous_questions  = body.get('previous_questions', None)

        if category != 0:
            question_list = Question.query.filter(Question.category == category).all()
        else:
            question_list = Question.query.all()

        for question in question_list[:]:
            if question.id in previous_questions:
                question_list.remove(question)

        if len(question_list) > 0:
            question = random.choice(question_list)

            current_question = {
                "id":           question.id,
                "question":     question.question,
                "answer":       question.answer,
                "difficulty":   question.difficulty,
                "category":     question.category
            }
        else:
            current_question = False

        return jsonify({
            'success': True,
            'question': current_question
        })




    # ----------------------------------------------------- #
    # --------------------- ERROR HANDLERS ---------------- #
    # ----------------------------------------------------- #
    
    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad Request"
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not Found"
            }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "Method Not Allowed"
            }), 405

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable Entity"
            }), 422



    return app

