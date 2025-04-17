
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from manager.models import Project, Task, TaskType, Tag, Comment

User = get_user_model()


class ProjectViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.client.login(username="testuser", password="pass")

        self.project = Project.objects.create(name="Test Project")
        self.task_type = TaskType.objects.create(name="Bug")

        Task.objects.create(name="A", project=self.project, task_type=self.task_type,
                            status="new", priority="High", deadline="2025-05-01", created_by=self.user)
        Task.objects.create(name="B", project=self.project, task_type=self.task_type,
                            status="done", priority="Low", deadline="2025-05-01", created_by=self.user)

    def test_project_list_view_adds_task_stats(self):
        response = self.client.get(reverse("manager:project-list"))
        project = response.context["projects"][0]
        self.assertEqual(project.total_tasks, 2)
        self.assertEqual(project.tasks_new, 1)
        self.assertEqual(project.tasks_done, 1)


class TaskCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="creator", password="1234")
        self.project = Project.objects.create(name="Proj")
        self.task_type = TaskType.objects.create(name="Feature")
        self.client.login(username="creator", password="1234")

    def test_task_number_autoincrements(self):
        Task.objects.create(name="Old", project=self.project, task_type=self.task_type,
                            number="F-001", priority="High", status="new",
                            deadline="2025-05-01", created_by=self.user)

        response = self.client.post(
            reverse("manager:task-create", kwargs={"project_id": self.project.id}),
            {
                "name": "New task",
                "description": "",
                "deadline": "2025-05-02",
                "status": "new",
                "priority": "Medium",
                "task_type": self.task_type.id,
            }
        )
        new_task = Task.objects.last()
        self.assertEqual(new_task.number, "F-002")


class TaskDetailStatusUpdateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="usr", password="pass")
        self.project = Project.objects.create(name="Test P")
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Some task", project=self.project, task_type=self.task_type,
            priority="Low", status="new", deadline="2025-05-01", created_by=self.user
        )
        self.client.login(username="usr", password="pass")

    def test_post_updates_status(self):
        url = reverse("manager:task-detail", kwargs={"pk": self.task.pk})
        self.client.post(url, {"status_update": "in_progress"})
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "in_progress")

    def test_comment_post_creates_comment(self):
        url = reverse("manager:task-detail", kwargs={"pk": self.task.pk})
        self.client.post(url, {"content": "Nice job!"})
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, "Nice job!")


class MyTaskListFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="assigned", password="123")
        other_user = User.objects.create_user(username="unassigned", password="123")

        self.task_type = TaskType.objects.create(name="T")
        project = Project.objects.create(name="P")

        self.task = Task.objects.create(
            name="Assigned", project=project, task_type=self.task_type,
            status="new", priority="High", deadline="2025-05-01", created_by=other_user
        )
        self.task.assignees.add(self.user)
        self.client.login(username="assigned", password="123")

    def test_my_tasks_shows_only_assigned(self):
        response = self.client.get(reverse("manager:my-tasks"))
        tasks = response.context["task_list"]
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, "Assigned")

    def test_filter_by_status(self):
        url = reverse("manager:my-tasks") + "?status=new"
        response = self.client.get(url, HTTP_HX_REQUEST="true")
        self.assertContains(response, "Assigned")

    def test_filter_by_priority(self):
        url = reverse("manager:my-tasks") + "?priority=High"
        response = self.client.get(url)
        self.assertContains(response, "Assigned")

    def test_filter_by_task_type(self):
        url = reverse("manager:my-tasks") + f"?task_type={self.task_type.id}"
        response = self.client.get(url)
        self.assertContains(response, "Assigned")
