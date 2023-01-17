# what-todo-django
a ToDo app written in Django

## Setup
#### Poetry
If you don't have [Poetry](https://python-poetry.org/) installed, run:

`curl -sSL https://install.python-poetry.org | python3 -`

1. Clone this repository and `cd` into the project root directory.
2. `poetry install`
3. create a local environment settings file: `touch .env`
4. Create entries for the following settings in your local .env file:
   * `SECRET_KEY`
5. `poetry run python manage.py migrate`
6. `poetry run python manage.py runserver`