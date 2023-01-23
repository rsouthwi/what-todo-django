from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, View, edit

from .models import ToDoList, Task

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
            todo_lists = ToDoList.objects.filter(user=self.request.user).order_by("-active", "-date_modified")
            for todo_list in todo_lists:
                todo_list.incomplete_tasks = todo_list.task_set.filter(completed=False).count()
            return todo_lists
        except TypeError:
            pass


class TodoListDetailView(DetailView):
    model = ToDoList
    template_name = "todo/detail.html"


class TodoListCreateView(edit.CreateView):
    model = ToDoList
    fields = ["title"]
    template_name = "todo/list-add.html"

    def form_valid(self, form):
        new_list = form.save(commit=False)
        new_list.user = self.request.user
        new_list.save()
        return HttpResponseRedirect(reverse_lazy("show-lists"))


class TodoListDeleteView(edit.DeleteView):
    model = ToDoList
    template_name = "todo/list-delete.html"
    success_url = reverse_lazy("show-lists")


class TodoListToggleActiveState(RedirectView):
    permanent = False
    url = reverse_lazy("show-lists")

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        slug = self.kwargs.get("slug")
        todo_list = ToDoList.objects.get(slug=slug)
        todo_list.active = False if todo_list.active else True
        todo_list.save()
        return response


class TaskToggleCompletedState(RedirectView):
    def get(self, request, *args, **kwargs):
        task_id = self.kwargs.get("task_id")
        task = Task.objects.get(id=task_id)
        task.completed = False if task.completed else True
        task.save()
        url = reverse_lazy("list-detail", kwargs={'slug': task.todo_list.slug})
        return HttpResponseRedirect(url)

class TaskCreateView(edit.CreateView):
    model = Task
    fields = ["name", "description"]
    template_name = "todo/list-add.html"

    def form_valid(self, form):
        slug = self.kwargs.get("slug")
        todo_list = ToDoList.objects.get(slug=slug)
        new_list = form.save(commit=False)
        new_list.todo_list = todo_list
        new_list.save()
        return HttpResponseRedirect(reverse_lazy("list-detail", kwargs={'slug': slug}))