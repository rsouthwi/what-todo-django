# what-todo-django
a ToDo app written in Django

## Requirements
#### This project requires [Poetry](https://python-poetry.org/)
If you don't have Poetry installed, run:

`curl -sSL https://install.python-poetry.org | python3 -`

## SetUp
1. Clone this repository and `cd` into the project root directory.
2. `poetry install`
3. create a local environment settings file: `touch .env`
4. generate a secret key:
	* `python -c 'import secrets; print(secrets.token_urlsafe())'`

4. Create entries, including values, for the following settings in your local .env file:
   * `SECRET_KEY={ value from previous step }`
5. `poetry run python manage.py migrate`
6. `poetry run python manage.py runserver`