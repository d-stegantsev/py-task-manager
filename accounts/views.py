from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("manager:project-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
