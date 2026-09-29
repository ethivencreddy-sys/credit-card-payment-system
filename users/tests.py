from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class AuthenticationTests(APITestCase):

    def test_user_registration(self):
        data = {
            "username": "testauth",
            "email": "testauth@example.com",
            "password": "TestPassword123"
        }

        response = self.client.post(
            "/api/auth/register/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(username="testauth").exists()
        )

    def test_user_login(self):
        User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="TestPassword123"
        )

        data = {
            "username": "loginuser",
            "password": "TestPassword123"
        }

        response = self.client.post(
            "/api/auth/login/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)