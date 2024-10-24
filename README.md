Rule Engine Flask Application
Overview
A Flask-based application for rule-based user eligibility evaluation using Abstract Syntax Trees (AST). This project allows users to define custom rules using logical and comparison operations on user attributes like age, department, and income. The application evaluates these rules against input data provided in JSON format.

What is a Rule Engine?
A rule engine enables users to define business logic in the form of rules that are evaluated against data to make decisions (e.g., granting access based on conditions like age and department).

Why Use AST?
An Abstract Syntax Tree (AST) provides a hierarchical representation of the structure of rules, making it easier to parse, process, and evaluate them.

Technologies Used
Flask: Lightweight web framework for building web applications.
AST: Python module to parse expressions and represent them as trees.
Python Operator Module: Defines comparison operations.

HTML/CSS: For rendering the user interface.
Project Features
Rule Creation: Users can enter custom rule strings (e.g., (age > 30 and department == 'Sales')).

Data Evaluation: Users provide JSON data (e.g., {"age": 35, "department": "Sales"}) to evaluate against defined rules.

User-Friendly Interface: Simple web interface for rule entry and evaluation.

Getting Started
Prerequisites
Python 3.8+
Flask (install via pip)

Usage at Final Output
Creating a Rule
Navigate to the home page (http://127.0.0.1:5000/).
Input a valid rule in the "Enter Rule String" field.
Click "Create Rule" to parse and store the rule.
Evaluating a Rule
Input JSON data to evaluate in the "Enter JSON Data for Evaluation" field.
Click "Evaluate Rule" to see if the data satisfies the rule.

Final Output Will be :
Testing a Rule Example:
If you enter the rule:
((age > 30 and department == 'Sales') or (age < 25 and department == 'Marketing')) and (salary > 50000 or experience > 5)
and click Create Rule, you should expect something like:
Rule Created: operator: AND

If you input the following JSON data:
{"age": 35, "department": "Sales", "salary": 60000, "experience": 6}
You should get:
{"result": true}
