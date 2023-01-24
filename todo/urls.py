from django.urls import path

from todo import views


urlpatterns = [
    path("", views.RootRedirectView.as_view()),
    path("lists/", views.TodoListView.as_view(), name="show-lists"),
    path("lists/add/", views.TodoListCreateView.as_view(), name="list-add"),
    path("lists/<slug:slug>/add/", views.TaskCreateView.as_view(), name="task-add"),
    path("lists/<slug:slug>/toggle-active/", views.TodoListToggleActiveState.as_view(), name="list-toggle-active"),
    path("lists/<slug:slug>/delete/", views.TodoListDeleteView.as_view(), name="list-delete"),
    path("lists/<slug:slug>/edit/", views.ToDoListUpdateView.as_view(), name="list-update"),
    path("lists/<slug:slug>/", views.TodoListDetailView.as_view(), name="list-detail"),
    path("tasks/<int:pk>/toggle-completed/", views.TaskToggleCompletedState.as_view(), name="task-toggle-complete"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task-update")
]