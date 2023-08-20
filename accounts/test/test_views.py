from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class UserSignUpTest(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.url = reverse_lazy("signup")

    @patch("accounts.views.services.user_create")
    def test_successfull_signup(self, mock_user_create):
        mock_user_create.return_value = self.User(email="test@example.com")

        response = self.client.post(
            self.url,
            {
                "email": "test@example.com",
                "password": "test1234",
                "confirm_password": "test1234",
                "account_type": "borrower",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_failed_signup(self):
        response = self.client.post(
            self.url,
            {
                "email": "test@example.com",
                "password": "1234",
                "confirm_password": "test1234",
                "account_type": "borrower",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
