from django.urls import path
from manager.views import (
    ProjectListView,
    ProjectCreateView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    MyTaskListView,
)

app_name = "manager"

urlpatterns = [
    # Project URLs
    path("", ProjectListView.as_view(), name="project-list"),
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),

    # Task list and creation (per project)
    path("projects/<int:project_id>/tasks/", TaskListView.as_view(), name="task-list"),
    path("projects/<int:project_id>/tasks/create/", TaskCreateView.as_view(), name="task-create"),

    # Task detail and update
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),

    # My tasks
    path("my-tasks/", MyTaskListView.as_view(), name="my-tasks"),
]
