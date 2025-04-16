from django.urls import path
from manager.views import (
    TaskListView,
    # MyTaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    # TaskDeleteView,
)


urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    # path("my/", MyTaskListView.as_view(), name="my-tasks"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    # path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]

app_name = "manager"
