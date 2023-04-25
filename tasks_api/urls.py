from django.urls import path
# from django.conf.urls import url
from .views import (
TaskListApiView,
)

urlpatterns = [
    path('api', TaskListApiView.as_view()),
]