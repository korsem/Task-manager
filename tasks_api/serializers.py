from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, TaskHistory
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name", "description", "status", "assigned_to"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class TaskHistorySerializer(serializers.ModelSerializer):
    local_timestamp = serializers.SerializerMethodField()

    class Meta:
        model = TaskHistory
        fields = ["task", "user", "local_timestamp", "changes"]

    # changing the format of the timestamp to more friendly
    def get_local_timestamp(self, obj):
        local_tz = timezone.get_current_timezone()
        return obj.timestamp.astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")
