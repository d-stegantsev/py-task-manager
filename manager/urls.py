from django.urls import path
from manager.views import (
    ProjectListView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    # MyTaskListView,
    # TaskDeleteView,
)

app_name = "manager"

urlpatterns = [
    # Projects
    path("", ProjectListView.as_view(), name="project-list"),

    # Tasks by project
    path("projects/<int:project_id>/tasks/", TaskListView.as_view(), name="task-list"),
    path("projects/<int:project_id>/tasks/create/", TaskCreateView.as_view(), name="task-create"),

    # Task detail / update
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),

    # path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    # path("my-tasks/", MyTaskListView.as_view(), name="my-tasks"),
]
