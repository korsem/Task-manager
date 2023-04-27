from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import TaskListApiView, TaskDetailApiView, ListUsers

urlpatterns = [
    path('api/users/', ListUsers.as_view()),
    path('api/', csrf_exempt(TaskListApiView.as_view())), # to be changed
    path('api/<int:task_id>/', TaskDetailApiView.as_view())
]
