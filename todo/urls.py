from django.urls import path

from todo import views

"""
Thoughts on urls for this app:
    we have an api and template-views
    api endpoints should be behind an api path
    template-views should not
    /todo/ - shows whichever active list has the most recent activity
    /todo/lists/ - list list view
    /todo/{list_slug}/ - list detail view

    restful api urls?
    /todo/api/list/ - GET, POST (create list)
    /todo/api/list/{list_slug}/ - GET, POST (add task?), DELETE, PATCH
    /todo/api/list/{list_slug}/{task_id} - POST (change state), DELETE, PUT
"""

urlpatterns = [
    # tempalte paths
    # path("/", ),
    path("lists/", views.TodoListView.as_view(), name="show-lists"),
    path("lists/add/", views.TodoListCreateView.as_view(), name="list-add"),
    path("lists/<slug:slug>/add/", views.TaskCreateView.as_view(), name="task-add"),
    path("lists/<slug:slug>/toggle-active/", views.TodoListToggleActiveState.as_view(), name="list-toggle-active"),
    path("lists/<slug:slug>/delete/", views.TodoListDeleteView.as_view(), name="list-delete"),
    path("lists/<slug:slug>/", views.TodoListDetailView.as_view(), name="list-detail"),
    path("tasks/<int:task_id>/toggle-completed/", views.TaskToggleCompletedState.as_view(), name="task-toggle-complete")


    #
    # # api paths
    # path("/api/list/", ),
    # path("/api/list/<slug:list_slug>/", ),
    # path("/api/list/<slug:list_slug>/<int:task_id>", )
]