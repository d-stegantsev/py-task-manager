from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Position

User = get_user_model()


class WorkerModelTests(TestCase):
    def test_create_user_with_position(self):
        position = Position.objects.create(name="QA")
        user = User.objects.create_user(
            username="tester",
            password="secure123!",
            position=position
        )
        self.assertEqual(user.username, "tester")
        self.assertEqual(user.position.name, "QA")


class SignUpViewTests(TestCase):
    def test_signup_form_registers_user(self):
        response = self.client.post(reverse("accounts:signup"), {
            "username": "alice",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="alice").exists())
