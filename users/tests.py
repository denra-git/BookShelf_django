from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserLogicTests(TestCase):

    def test_user_can_login(self):
        User.objects.create_user(
            username="user",
            password="pass123",
        )

        response = self.client.post(
            reverse("users:login"),
            {
                "username": "user",
                "password": "pass123",
            },
        )

        self.assertRedirects(
            response,
            reverse("users:profile"),
        )

        self.assertTrue(
            self.client.session.get("_auth_user_id")
        )

    def test_user_cannot_login_with_invalid_credentials(self):
        User.objects.create_user(
            username="user",
            password="pass123",
        )

        response = self.client.post(
            reverse("users:login"),
            {
                "username": "user",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            self.client.session.get("_auth_user_id")
        )

    def test_user_can_logout(self):
        user = User.objects.create_user(
            username="user",
            password="pass123",
        )

        self.client.force_login(user)

        response = self.client.get(
            reverse("users:logout")
        )

        self.assertRedirects(
            response,
            reverse("users:login"),
        )

        self.assertFalse(
            self.client.session.get("_auth_user_id")
        )

    def test_user_can_register(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "username": "new_user",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(
            response,
            reverse("users:profile"),
        )

        self.assertTrue(
            User.objects.filter(
                username="new_user"
            ).exists()
        )

        self.assertTrue(
            self.client.session.get("_auth_user_id")
        )

    def test_authenticated_user_is_redirected_from_login(self):
        user = User.objects.create_user(
            username="user",
            password="pass123",
        )

        self.client.force_login(user)

        response = self.client.get(
            reverse("users:login")
        )

        self.assertRedirects(
            response,
            reverse("users:profile"),
        )

    def test_authenticated_user_can_access_profile(self):
        user = User.objects.create_user(
            username="user",
            password="pass123",
        )

        self.client.force_login(user)

        response = self.client.get(
            reverse("users:profile")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_anonymous_user_is_redirected_from_profile(self):
        response = self.client.get(
            reverse("users:profile")
        )

        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next=/users/profile/",
        )