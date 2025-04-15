from django.contrib import admin
from .models import Position, Worker, TaskType, Task, Tag, Comment


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "position")
    search_fields = ("username", "email")
    list_filter = ("position",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "priority", "deadline", "created_by")
    list_filter = ("status", "priority", "task_type", "tags")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees", "tags")
    readonly_fields = ("created_time", "updated_time")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "created_by", "created_time")
    search_fields = ("content",)
    list_filter = ("created_time",)
