from django.urls import path
from .views import (
    TaskListApiView,
    TaskDetailApiView,
    ListUsers,
    UserTasksView,
    SearchTasksView,
    FilterTasksView
)

urlpatterns = [
    path('api/users/', ListUsers.as_view()),
    path('api/users/<int:user_id>/', UserTasksView.as_view()),
    path('api/', TaskListApiView.as_view()),
    path('api/<int:task_id>/', TaskDetailApiView.as_view()),
    path('api/search/<str:q>/', SearchTasksView.as_view()),
    path('api/search/<str:field>/<str:q>/', FilterTasksView.as_view())
]
