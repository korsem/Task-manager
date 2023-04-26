from django.urls import path
# from django.conf.urls import url
from .views import (
    TaskListApiView,
    TaskDetailApiView
)

urlpatterns = [
    path('api', TaskListApiView.as_view()),
    path('api/<int:task_id>/', TaskDetailApiView.as_view())
]