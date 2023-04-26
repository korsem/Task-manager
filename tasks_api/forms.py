from django import forms
from django.contrib.auth.models import User
from .models import Task
class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ["name", "description", "status", "assigned_to"]