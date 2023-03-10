import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_NAME_TEST, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.database_name = DB_NAME_TEST
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USER, DB_PASSWORD, "localhost:5432", self.database_name
        )

        self.app = create_app(self.database_path)
        self.client = self.app.test_client

        self.new_trivia = {
            "id": 1,
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
        res = self.client().get("/categories/1000/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    # TESTS FOR [POST '/questions']
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_trivia)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))

    # TESTS FOR [DELETE '/questions/<question_id>']
    def test_delete_question(self):
        res = self.client().delete("/questions/1")
        data = json.loads(res.data)
    
        with self.app.app_context():
            question_id = 1
            question = Question.query.filter(Question.id == question_id -1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 1)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(question, None)


    # TESTS FOR [POST '/questions/search']
    def test_get_question_search_with_results(self):
        res = self.client().post("/questions/search", json={"searchTerm": "Which"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(len(data["questions"]), 7)

    def test_get_question_search_without_results(self):
        res = self.client().post("/questions/search", json={"searchTerm": "banana bread"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()