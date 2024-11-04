from django.urls import path

from apps.tasks.views import *

urlpatterns = [
    path('tasks/list/', ListTaskApi.as_view(), name='list_task'),
    path('tasks/add/', AddTaskApi.as_view(), name='add_task'),
    path('tasks/modify/status/info/', ModifyTaskStatusInfoApi.as_view(), name='modify_task_status_info'),
    path('tasks/modify/status/stop/', ModifyTaskStatusStopApi.as_view(), name='modify_task_status_stop'),
    path('tasks/modify/status/start/', ModifyTaskStatusStartApi.as_view(), name='modify_task_status_start'),
]
