from django.shortcuts import render

from django.views.generic import ListView, DetailView
from manager.models import Task


class TaskListView(ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "manager/task_list.html"

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type", "created_by").prefetch_related("assignees", "tags")
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_filter"] = self.request.GET.get("status", "")
        context["status_choices"] = Task.Status.choices
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = "manager/task_detail.html"
    context_object_name = "task"
