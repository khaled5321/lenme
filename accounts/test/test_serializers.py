from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..serializers import UserSerializer


class UserSerializerTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.serializer_class = UserSerializer

    def test_valid_password(self):
        serializer = self.serializer_class(
            data={
                "email": "test@example.com",
                "password": "test1234",
                "confirm_password": "test1234",
                "account_type": "borrower",
            }
        )
        self.assertTrue(serializer.is_valid())

    def test_invalid_numeric_password(self):
        serializer = self.serializer_class(
            data={
                "email": "test@example.com",
                "password": "1234",
                "confirm_password": "1234",
                "account_type": "borrower",
            }
        )

        self.assertFalse(serializer.is_valid())

    def test_invalid_password_raise_exception(self):
        serializer = self.serializer_class(
            data={
                "email": "test@example.com",
                "password": "1234",
                "confirm_password": "1234",
                "account_type": "borrower",
            }
        )
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_passwords_match(self):
        serializer = self.serializer_class(
            data={
                "email": "test@example.com",
                "password": "test1234",
                "confirm_password": "test1234",
                "account_type": "borrower",
            }
        )
        self.assertTrue(serializer.is_valid())

    def test_passwords_dont_match(self):
        serializer = self.serializer_class(
            data={
                "email": "test@example.com",
                "password": "test1234",
                "confirm_password": "test4321",
                "account_type": "borrower",
            }
        )
        self.assertFalse(serializer.is_valid())
