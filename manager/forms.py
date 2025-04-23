from django import forms
from django.utils import timezone
from manager.models import Comment, Task, Project


# Project creation/edit form
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "deadline"]
        widgets = {
            "deadline": forms.DateInput(
                attrs={"type": "date", "class": "form-control no-timepicker"}
            ),
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        # Prevent setting a past date for project deadline
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline


# Comment form for tasks
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Write a comment...",
                }
            ),
        }


# Task creation/edit form
class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "status",
            "priority",
            "task_type",
            "assignees",
            "tags",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 5, "class": "form-control"}),
            "deadline": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Pick date and time",
                },
                format="%Y-%m-%d %H:%M",
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "assignees": forms.CheckboxSelectMultiple,
            "tags": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.deadline:
            self.initial["deadline"] = self.instance.deadline.strftime(
                "%Y-%m-%d %H:%M"
            )

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        # Prevent setting a past datetime for task deadline
        if deadline and deadline < timezone.now():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline
