from django.contrib.auth.models import User
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(unique=True)
    users = models.ManyToManyField(User, related_name='projects')
    is_deleted = models.BooleanField(default=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')])
    due_date = models.DateField()
    permission = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
