from django.db import models

# Create your models here.

"""
Ideas for Models and/or data entities:
User
    name
ToDoList
    title - str
    slug - slug
    date created - datetime
    date modified - datetime
    user - FK
    active - bool
Task
    - todo_list - fk
    - task_name - str
    - task_description - optional text
    - completed - bool
    - date created
    - date completed
"""