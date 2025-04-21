from django import forms
from manager.models import Comment, Task, Project


# Project creation/edit form
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "deadline"]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }


# Comment form for tasks
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write a comment..."
            }),
        }


# Task creation/update form
class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
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
                    "type": "datetime-local",
                }
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "assignees": forms.CheckboxSelectMultiple,
            "tags": forms.CheckboxSelectMultiple,
        }
