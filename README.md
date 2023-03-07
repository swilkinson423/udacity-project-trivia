# API Development and Documentation Final Project

## Trivia App API




`GET '/questions'`

- Fetches a list of paginated questions. 
- Each 'page' will list up to 10 questions. If no 'page' is stated, the default is Page 1. 
- Required Request Arguments: None
- Optional Request Arguments: 'page' (ex: `'/questions?page=2'`)
- Returns: A json with the following keys: 
    `'success'` (return value: True or False),  
    `'questions'` (return value: an array of the questions on the current page), 
    `'total_questions'` (return value: the total number of questions), 
    `'categories'` (return value: an array of the names of the categories), 
    `'current_category'` (return value: the ID of the current category)

    ```json
    {
    "success": True,
    "questions": [<question 01>,<question02>],
    "total_questions": 10,
    "categories": ["History","Science","Art"],
    "current_category": 0
    }
    ```



`GET '/categories'`

- Fetches a list of all categories by name.
- Request Arguments: None
- Returns: A json with keys `'success'` (return value: True or False) and `'categories'` (return value: an array of the names of the categories)



`GET '/categories/<category_id>/questions'`

- Fetches the paginated selection of questions for the selected category.
- Each 'page' will list up to 10 questions. If no 'page' is stated, the default is Page 1. 
- Required Request Arguments: 'category_id' 
- Optional Request Arguments: 'page' (ex: `'/categories/2/questions?page=2'`)
- Returns: A json with the following keys: 
    `'success'` (return value: True or False),  
    `'questions'` (return value: an array of the questions on the current page), 
    `'total_questions'` (return value: the total number of questions), 
    `'categories'` (return value: an array of the names of the categories), 
    `'current_category'` (return value: the ID of the current category)



`DELETE '/questions/<question_id>'`

- Deletes a questions based on the question's ID.
- Required Request Arguments: 'question_id' (ex: `'/questions/3'`)
- Returns: A json with the following keys:
    `'success'` (return value: True or False),  
    `'questions'` (return value: an array of the questions on the current page), 
    `'total_questions'` (return value: the total number of questions), 
    `'categories'` (return value: an array of the names of the categories), 
    `'current_category'` (return value: the ID of the current category)



`POST '/questions'`

- Posts a new question to the database.
- Required Request Arguments: 
    'question'      - The text of the question (String),
    'answer'        - The text of the answer (String),
    'difficulty'    - The difficulty from 1-5 (Int),
    'category'      - The ID of the category (Int)
- Returns: A json with the following keys:
    `'success'` (return value: True or False),  
    `'created'` (return value: the created question)
    `'questions'` (return value: an array of the questions on the current page), 
    `'total_questions'` (return value: the total number of questions), 
    `'categories'` (return value: an array of the names of the categories), 
    `'current_category'` (return value: the ID of the current category)



`POST '/questions/search'`

- Returns the list of questions matching a search term.
- Required Request Arguments: 'searchTerm' (ex: `'/questions/search?searchTerm="movie"'`)
- Optional Request Arguments: 'page'
- Returns: A json with the following keys:
    `'success'` (return value: True or False),  
    `'questions'` (return value: an array of the questions matching the search term, paginated), 
    `'total_questions'` (return value: the total number of questions), 
    `'categories'` (return value: an array of the names of the categories), 
    `'current_category'` (return value: the ID of the current category)