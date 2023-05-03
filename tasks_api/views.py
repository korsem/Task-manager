from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task, TaskHistory
from .serializers import TaskSerializer, TaskHistorySerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.db.models import Q


# Home api View
class HomeApiView(APIView):
    def get(self, request):
        data = {'message': 'Task manager is the basic CRUD app for managing tasks. <br> <br>'
                           'By setting up the certain HTTP API Endpoints you can list existing tasks, '
                           'add new one or delete an old one, you can also modify the existing one. <br> '
                           'Moreover, you can search for a specific task by a keyword '
                           'and access the history of the task changes. <br><br>'
                            '<small>To get to know about a specific endpoinds you need to use see README</small>'
                }

        return render(request, 'home.html', data)


# View for listing the users (every user has an access to it)
class ListUsers(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


# View for listing tasks assigned to a particular user
class UserTasksView(APIView):
    def get(self, request, user_id):
        tasks = Task.objects.filter(assigned_to=user_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


# View for listing all the tasks
class TaskListApiView(APIView):

    # adding permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # get for listing all the tasks
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # creating the new task with given data
    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'status': request.data.get('status', 'Nowy'),
            'assigned_to': request.data.get('assigned_to')
        }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view for displaying the results of a specific task
class TaskDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # method returns the objects for requested user
    def get_object_user(self, task_id):
        task_instance = Task.objects.filter(id=task_id, assigned_to=self.request.user.id).first()
        return task_instance

    # method returns all objects
    def get_object(self, task_id):
        task_instance = Task.objects.filter(id=task_id).first()
        return task_instance

    # retrieve task with given task_id if exist
    def get(self, request, task_id, *args, **kwargs):
        task_instance = self.get_object(task_id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TaskSerializer(task_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update every field of task with given task id if exists (except id)
    def put(self, request, task_id, *args, **kwargs):
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
            user = request.user if request else None
            task_history = TaskHistory.objects.create(task=task_instance, user=user, changes=serializer.validated_data)
            serializer.save()
            task_history.changes = serializer.validated_data
            task_history.save()  # creating a new instance of task_history
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update task with given task id if exist, updating chosen fields
    def patch(self, request, task_id, *args, **kwargs):

        task_instance = self.get_object(task_id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exist"}
            )
        serializer = TaskSerializer(instance=task_instance, data=request.data, partial=True,
                                    context={'request': request})
        if serializer.is_valid():
            user = request.user if request else None
            task_history = TaskHistory.objects.create(task=task_instance, user=user, changes=serializer.validated_data)
            serializer.save()
            task_history.changes = serializer.validated_data
            task_history.save()  # creating a new instance of task_history
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # deletes the given task with task_id if exists
    def delete(self, request, task_id, *args, **kwargs):

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
    def get(self, request, q):  # check if the parameter is in th description field or name field
        tasks = Task.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

# filtering and searching by a keyword in a given field
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
        # then if field is valid there is a filter condition "field:q", where q is a filter keyword
        filter_condition = Q(**{fields[field]: q})
        tasks = Task.objects.filter(filter_condition)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


# View for listing the history of changes for a given task
class HistoryTaskView(APIView):
     def get(self, request, task_id):
         task = Task.objects.get(id=task_id)
         changes = TaskHistory.objects.filter(task=task).order_by('timestamp')
         serializer = TaskHistorySerializer(changes, many=True)
         return Response(serializer.data)
