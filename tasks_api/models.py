from django.db import models
from django.contrib.auth.models import User
# in this file comments are in polish
class Task(models.Model):
    NEW = 'Nowy'
    IN_PROGRESS = 'W toku'
    RESOLVED = 'Rozwiązany'
    STATUS_CHOICES = [ # lista 3 mozliwych wartosci statusu
        (NEW, 'Nowy'),
        (IN_PROGRESS, 'W toku'),
        (RESOLVED, 'Rozwiązany'),
    ]
    id = models.AutoField(primary_key=True)  # id - kolejno nadawany numer
    name = models.CharField(max_length=128, blank=False, null=False) # nazwa
    description = models.TextField(blank=True, null=True) # opis
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW) # status - korzystam ze wczesniej utworzonej listy
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) # przypisany uzytkowik - pole opcjonalne, a w przypadku usuniecia przypisania ustawiam wartosc na NULL

    # zwraca nazwe zadania
    def __str__(self):
        return self.name

# Model pomocniczy do przechowywania historii zmian danego zadania
class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history") # klucz obcy na zadanie (tzn ktorego zadanie jest to historia zmian)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # przechowuje Usera, ktory dokonal zmiany
    timestamp = models.DateTimeField(auto_now_add=True) # dokladny czas zmiany
    changes = models.JSONField() # informacja jaka zmiana zostala wprowadzona