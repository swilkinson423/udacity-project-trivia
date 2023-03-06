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
        
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )

        self.app = create_app(self.database_path)
        self.client = self.app.test_client

        self.new_trivia = {
            "question": "Who let the dogs out?",
            "answer": "The Baja Men...I think",
            "category": 1,
            "difficulty": 5
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # TODO: TEST FOR GET QUESTIONS
    # TODO: TEST FOR GET QUESTIONS (ERROR 404)
    # TODO: TEST FOR GET CATEGORIES
    # TODO: TEST FOR GET QUESTIONS IN CATEGORY
    # TODO: TEST FOR DELETE QUESTION
    # TODO: TEST FOR DELETE QUESTION (ERROR 404)
    # TODO: TEST FOR DELETE QUESTION (ERROR 422)
    # TODO: TEST FOR POST QUESTION
    # TODO: TEST FOR POST QUESTION (ERROR 422)
    # TODO: TEST FOR POST QUESTION (ERROR 400)
    # TODO: TEST FOR SEARCH QUESTION
    # TODO: TEST FOR SEARCH QUESTION (ERROR 400)
    # TODO: TEST FOR START QUIZ (ALL QUESTIONS)
    # TODO: TEST FOR START QUIZ (CATEGORY QUESTIONS)
    




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()