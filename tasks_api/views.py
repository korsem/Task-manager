from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Task
from .serializers import TaskSerializer
from django import forms
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

class TaskListApiView(APIView):
    # adding permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # get for listing all the tasks for given requested user
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(assigned_to = request.user.id)
        serializer = TaskSerializer(tasks, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    # creating the new task with given data
    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = form.cleaned_data['assigned_to']
            task.save()
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailApiView(APIView):
    # adding permission to check if user is authnticated
    permission_classes = [permissions.IsAuthenticated]
    # retrieve
    def get_object(self, request, task_id, *args, **kwargs):
        task_instance = self.get_object(task_id, request.user.id)
        if not task_instance:
            return Response(
                {"rest": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TaskSerializer(task_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update
    def put(self, request, task_id, *args, **kwargs):
        # update task with given task id if exist
        task_instance = self.get_object(task_id, request.user.id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exist"}
            )
        data = {  # check i dont need the other fields
            'name': request.data.get('name'),
            'assigned_to': request.user.id,
        }
        serializer = TaskSerializer(instance=task_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete
    def delete(self, request, task_id, *args, **kwargs):
        # deletes the given task with task_id if exists
        task_instance = self.get.object(task_id, request.user.id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        task_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
