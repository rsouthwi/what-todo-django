from django.contrib import admin
from .models import Task, ToDoList

class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'active')
    list_filter =  ('user', 'active', 'date_modified')

admin.site.register(Task)
admin.site.register(ToDoList, ToDoListAdmin)
