from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin

from manager.forms import CommentForm, TaskForm
from manager.models import Task, Comment, Worker


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


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:task-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        type_name = form.cleaned_data["task_type"].name
        prefix = "".join(word[0] for word in type_name.split()).upper()

        count = Task.objects.filter(task_type=form.cleaned_data["task_type"]).count() + 1
        form.instance.number = f"{prefix}-{count:03d}"

        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:task-list")


class SignUpView(CreateView):
    model = Worker
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("manager:task-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response