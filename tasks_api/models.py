from django.db import models
from django.contrib.auth.models import User
class Task(models.Model):
    NEW = 'Nowy'
    IN_PROGRESS = 'W toku'
    RESOLVED = 'Rozwiązany'
    STATUS_CHOICES = [ # list of three possible status choices (status jako lista 3 mozliwosci)
        (NEW, 'Nowy'),
        (IN_PROGRESS, 'W toku'),
        (RESOLVED, 'Rozwiązany'),
    ]
    id = models.AutoField(primary_key=True)  # id (kolejno nadawany numer)
    name = models.CharField(max_length=128, blank=False, null=False) # name of the task (nazwa - krótki zwięzły tekst)
    description = models.TextField(blank=True, null=True) # discription of the dask (opis - dłuższy tekst)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW) # task status - I am using STATUS_CHOICES (status może przyjmować jedną z 3 wartości)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, default=None) # assigned user - optional field, and I set the value to NULL if the assignment is deleted (przypisany uzytkwnik)

    # returns the name of the task
    def __str__(self):
        return self.name
