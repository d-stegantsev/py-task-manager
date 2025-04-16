from django import forms
from manager.models import Comment, Task


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write a comment..."
            })
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "project",  # ← ДОДАЛИ
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
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
            "assignees": forms.CheckboxSelectMultiple,
            "tags": forms.CheckboxSelectMultiple,
        }

