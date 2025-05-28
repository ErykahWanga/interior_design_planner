Interior Design Planner


A Python CLI application for planning interior designs, managing rooms, furniture, and categories using SQLAlchemy ORM and SQLite.


Setup

Install Pipenv: pip install pipenv
Navigate to project directory: cd interior_design_planner
Install dependencies: pipenv install
Activate virtual environment: pipenv shell
Run the application: pipenv run python main.py

Features

Create, update, and delete rooms with dimensions.
Add and delete furniture with cost and category (e.g., Seating, Storage).
View room details with furniture list, categories, and total cost.

Usage

Choose options 1-8 from the CLI menu to manage rooms, furniture, and categories.
Follow prompts to input data (e.g., room name, furniture cost).

Database

SQLite database: interior_design.db
Tables: rooms, furniture, categories

