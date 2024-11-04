from django.urls import path

from apps.tasks.views import *

urlpatterns = [
    path('tasks/add/', AddTaskApi.as_view(), name='add_task'),
]
