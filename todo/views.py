import logging

from django.views.generic import ListView, TemplateView, DetailView, View

from .models import ToDoList

"""
Ideas for views:
user-scope
    - [GET] show active list with most recent activity (detail view)
        show form with list of items (including state)
        click on item to reveal details?
    - [GET] list dashboard (the default if there are no active lists)
        filter by active
        search by name
        sort by date
    - [POST] create new list
list-scope
    - [GET] list detail view (same as show active list above)
    - [POST] add list view (api endpoint?)
    - [DELETE] delete list (api endpoint?)
    - [PATCH] update list (api endpoint?)
        ° rename list
    - [POST] add task to list
task-scope
    - [POST] alter state of task (completed)
    - [DELETE] delete task, 
    - [PUT] change task:
        ° name
        ° description
        ° associated list
        ° completion state
"""
class TodoListView(ListView):
    context_object_name = "todo_lists"
    template_name = "todo/list.html"

    def get_queryset(self):
        try:
            return ToDoList.objects.filter(user=self.request.user).order_by("-active", "-date_modified")
        except TypeError:
            pass

class TodoListDetailView(DetailView):
    model = ToDoList
    template_name = "todo/detail.html"