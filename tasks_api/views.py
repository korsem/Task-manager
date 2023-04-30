from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.db.models import Q

# Home api View
class HomeApiView(APIView):
    def get(self, request):
        data = {'message': 'This is a home for Task management app. <br> To see access the list of users get /api/users <br> To see the tasks get /api/ <br> To see the details of the task get /api/<task_id>'}
        return render(request, 'home.html', data)

# Every user has an accesss to list users
class ListUsers(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

# listing tasks assigned to a particular user
class UserTasksView(APIView):
    def get(self, request, user_id):
        tasks = Task.objects.filter(assigned_to=user_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

# View for listing all of the tasks
class TaskListApiView(APIView):

    # adding permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # get for listing all the tasks
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    # creating the new task with given data
    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'status': request.data.get('status', 'Nowy'),
            'assigned_to': request.data.get('assigned_to')
        }
        print(data)
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# view for displaying the results of a specific task
# only available if the task belogs to a checking person to be changed problably
class TaskDetailApiView(APIView):
    # adding permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, task_id):
        task_instance = Task.objects.filter(id=task_id, assigned_to=self.request.user.id).first()
        return task_instance

    def get(self, request, task_id, *args, **kwargs):
        # retrieve task with given task_id if exist
        task_instance = self.get_object(task_id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TaskSerializer(task_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, task_id, *args, **kwargs):
        # update every field of task with given task id if exists
        task_instance = self.get_object(task_id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exist"}
            )
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'status': request.data.get('status', 'Nowy'),
            'assigned_to': request.data.get('assigned_to')
        }
        serializer = TaskSerializer(instance=task_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # partial update
    def patch(self, request, task_id, *args, **kwargs):
        # update task with given task id if exist, updating chosen fields
        task_instance = self.get_object(task_id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exist"}
            )
        serializer = TaskSerializer(instance=task_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete
    def delete(self, request, task_id, *args, **kwargs):
        # deletes the given task with task_id if exists
        task_instance = self.get_object(task_id,)
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

# filtering and searching by a keyword in either description or name
class SearchTasksView(APIView):
    def get(self, request, q):
        tasks = Task.objects.filter(Q(name__icontains=q) | Q(description__icontains=q)) # check if the parameter is in th desription field or name field
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class FilterTasksView(APIView):
    def get(self, request, field, q):
        fields = {
            "id": "id",
            "name": "name__icontains",
            "description": "description__icontains",
            "status": "status__iexact",
            "assigned_to": "assigned_to__username__iexact"
        }
        if field not in fields:
            return Response({"error": f"Invalid field '{field}'"}, status=400)
        # then if field is valid i have filter contition "field:q", where q is a filter keyword
        filter_condition = Q(**{fields[field]: q})
        tasks = Task.objects.filter(filter_condition)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

