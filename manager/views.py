from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from manager.forms import CommentForm
from manager.models import Task, Comment


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


class TaskDetailView(FormMixin, DetailView):
    model = Task
    template_name = "manager/task_detail.html"
    context_object_name = "task"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("manager:task-detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["comments"] = Comment.objects.filter(task=self.object).select_related("created_by").order_by("-created_time")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = self.object
            comment.created_by = self.request.user
            comment.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
