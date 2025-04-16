from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name="workers")

    def __str__(self):
        return self.username


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    priority = models.CharField(max_length=10)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="assigned_tasks"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_tasks"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return f"{self.name} [{self.status}]"


class Comment(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment by {self.created_by} on {self.task}"
