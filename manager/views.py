from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin

from manager.forms import CommentForm, TaskForm, ProjectForm
from manager.models import Task, Comment, Project, TaskType


class ProjectListView(ListView):
    model = Project
    template_name = "manager/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("tasks")
        for project in queryset:
            # Annotate project with task counts
            project.total_tasks = project.tasks.count()
            project.tasks_new = project.tasks.filter(status="new").count()
            project.tasks_in_progress = project.tasks.filter(status="in_progress").count()
            project.tasks_done = project.tasks.filter(status="done").count()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = date.today()
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "manager/project_form.html"
    success_url = reverse_lazy("manager:project-list")


class FilteredTaskListMixin:
    """Mixin for filtering tasks by status, priority, and type."""

    def filter_tasks(self, queryset):
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")
        task_type = self.request.GET.get("task_type")

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if task_type:
            queryset = queryset.filter(task_type_id=task_type)

        return queryset


class TaskListView(FilteredTaskListMixin, ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "manager/task_list.html"

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        queryset = Task.objects.filter(project_id=project_id).select_related(
            "task_type", "created_by"
        ).prefetch_related("assignees", "tags")
        return self.filter_tasks(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "status_choices": Task.Status.choices,
            "priority_choices": ["High", "Medium", "Low"],
            "status_filter": self.request.GET.get("status", ""),
            "priority_filter": self.request.GET.get("priority", ""),
            "task_type_filter": self.request.GET.get("task_type", ""),
            "task_types": TaskType.objects.all(),
            "project": Project.objects.get(pk=self.kwargs["project_id"]),
            "now": timezone.now(),
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.htmx:
            return self.response_class(
                request=self.request,
                template="includes/task_list_content.html",
                context=context,
                **response_kwargs
            )
        return super().render_to_response(context, **response_kwargs)


class TaskDetailView(FormMixin, DetailView):
    model = Task
    template_name = "manager/task_detail.html"
    context_object_name = "task"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("manager:task-detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "project": self.object.project,
            "form": CommentForm(),
            "comments": Comment.objects
            .filter(task=self.object)
            .select_related("created_by")
            .order_by("-created_time"),
            "came_from": self.request.GET.get("from", ""),
            "now": timezone.now(),
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if "status_update" in request.POST:
            new_status = request.POST.get("status_update")
            if new_status in dict(Task.Status.choices):
                self.object.status = new_status
                self.object.save()
            return self.get(request, *args, **kwargs)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = self.object
            comment.created_by = request.user
            comment.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"

    def form_valid(self, form):
        project_id = self.kwargs["project_id"]
        task_type = form.cleaned_data["task_type"]
        form.instance.created_by = self.request.user
        form.instance.project_id = project_id

        prefix = task_type.name[0].upper()
        existing_numbers = Task.objects.filter(
            project_id=project_id,
            task_type=task_type,
            number__startswith=f"{prefix}-"
        ).values_list("number", flat=True)
        used_numbers = []
        for num in existing_numbers:
            try:
                used_numbers.append(int(num.split("-")[1]))
            except (IndexError, ValueError):
                continue

        next_number = max(used_numbers, default=0) + 1
        form.instance.number = f"{prefix}-{next_number:03}"

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = Project.objects.get(pk=self.kwargs["project_id"])
        context["task"] = self.object if self.object else Task()
        return context

    def get_success_url(self):
        return reverse("manager:task-list", kwargs={"project_id": self.object.project_id})


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.object
        return context

    def get_success_url(self):
        return reverse("manager:task-detail", kwargs={"pk": self.object.pk})


class MyTaskListView(FilteredTaskListMixin, ListView):
    model = Task
    template_name = "manager/my_task_list.html"
    context_object_name = "task_list"

    def get_queryset(self):
        queryset = Task.objects.filter(
            assignees=self.request.user
        ).select_related("project", "task_type").order_by("project__name", "deadline")
        return self.filter_tasks(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "status_choices": Task.Status.choices,
            "priority_choices": ["High", "Medium", "Low"],
            "status_filter": self.request.GET.get("status", ""),
            "priority_filter": self.request.GET.get("priority", ""),
            "task_type_filter": self.request.GET.get("task_type", ""),
            "task_types": TaskType.objects.all(),
            "filter_url": reverse("manager:my-tasks"),
            "now": timezone.now(),
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.htmx:
            return self.response_class(
                request=self.request,
                template="includes/task_list_content.html",
                context=context,
                **response_kwargs
            )
        return super().render_to_response(context, **response_kwargs)
