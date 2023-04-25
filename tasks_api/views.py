from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Task
from .serializers import TaskSerializer

class TaskListApiView(APIView):
    # adding permission to check if user is authnticated
    permission_classes = [permissions.IsAuthenticated]

    # get for listing all the tasks for given requested user
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(assigned_to = request.user.id)
        serializer = TaskSerializer(tasks, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # creating the new task with given data
        data = {
            'name': request.data.get('name'),
            'assigned_to': request.user.id
        }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

