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

    # TESTS FOR [GET '/questions']
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    # TESTS FOR [GET '/categories']
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
    
    # TESTS FOR [GET '/categories/<category_id>/questions']
    def test_get_questions_by_category(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["current_category"], 2)

    def test_get_questions_category_out_of_bounds(self):
        print("OUT OF BOUNDS")
        res = self.client().get("/categories/1000/questions")
        data = json.loads(res.data)

        print(res.status_code)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")


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