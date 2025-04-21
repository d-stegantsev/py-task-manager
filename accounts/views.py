from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.models import Worker


class SignUpView(CreateView):
    model = Worker
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("manager:task-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
