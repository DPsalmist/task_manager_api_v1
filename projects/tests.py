# from django.contrib.auth.models import User
# from rest_framework.test import APITestCase
# from rest_framework import status
# from .models import Project

# class ProjectAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="password")
#         self.client.login(username="testuser", password="password")

#     def test_create_project(self):
#         data = {"name": "Test Project", "description": "Test"}
#         response = self.client.post("/api/projects/", data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Project.objects.count(), 1)

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Project

class ProjectAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )

        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Set Authorization header
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

    def test_create_project(self):
        data = {
            "name": "Test Project",
            "description": "Test Description"
        }

        response = self.client.post("/api/projects/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
