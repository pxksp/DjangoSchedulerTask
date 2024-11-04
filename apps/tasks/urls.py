from django.urls import path

from apps.tasks.views import *

urlpatterns = [
    path('', AddTaskApi.as_view(), name='add_task'),
]
