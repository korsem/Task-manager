from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
class Task(models.Model):
    NEW = 'Nowy'
    IN_PROGRESS = 'W toku'
    RESOLVED = 'Rozwiązany'
    STATUS_CHOICES = [ # lista 3 mozliwych wartosci zmiennych
        (NEW, 'Nowy'),
        (IN_PROGRESS, 'W toku'),
        (RESOLVED, 'Rozwiązany'),
    ]
    id = models.AutoField(primary_key=True)  # id - kolejno nadawany numer
    name = models.CharField(max_length=128, blank=False, null=False) # nazwa
    description = models.TextField(blank=True, null=True) # opis
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW) # status - korzystam ze wczesniej utworzonych zmiennych
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) # przypisany uzytkowik - pole opcjonalne, a w przypadku usuniecia przypisania ustawiam wartosc na NULL

    # zwraca nazwe zadania
    def __str__(self):
        return self.name

class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history") # History of which task
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # user who has made the change most recenly
    timestamp = models.DateTimeField(auto_now_add=True) # time of change
    changes = models.JSONField() # info about th change