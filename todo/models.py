from autoslug import AutoSlugField

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

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

class ToDoList(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    date_modified = models.DateTimeField(auto_now=True, blank=True, null=False)
    title = models.CharField(max_length=128)
    slug = AutoSlugField(populate_from="title", max_length=64, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)


class Task(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    date_modified = models.DateTimeField(auto_now=True, blank=True, null=False)
    todo_list = models.ForeignKey('ToDoList', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)