from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import TaskListApiView, TaskDetailApiView, ListUsers, UserTasksView, StatusTasksView

urlpatterns = [
    path('api/users/', ListUsers.as_view()),
    path('api/users/<int:user_id>/', UserTasksView.as_view()),
    path('api/', TaskListApiView.as_view()),
    path('api/<int:task_id>/', TaskDetailApiView.as_view()),
    path('api/search/<str:status>/', StatusTasksView.as_view())
]
