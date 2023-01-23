from django.urls import path

from .views import TodoListView, TodoListDetailView
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
    path("lists/", TodoListView.as_view()),
    path("lists/<slug:slug>/", TodoListDetailView.as_view(), name="list-detail"),
    #
    # # api paths
    # path("/api/list/", ),
    # path("/api/list/<slug:list_slug>/", ),
    # path("/api/list/<slug:list_slug>/<int:task_id>", )
]