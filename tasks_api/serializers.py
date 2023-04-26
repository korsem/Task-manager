from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class TaskSerializer(serializers.ModelSerializer):
    # assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ["id", "name", "description", "status", "assigned_to"]

