from django.test import TestCase
from unittest.mock import patch
from ..services import user_create


class TestUserCreate(TestCase):
    def test_user_create(self):
        data = {
            "email": "test@example.com",
            "account_type": "lender",
            "password": "password123",
        }

        with patch("accounts.services.User.save") as mock_save:
            user = user_create(data=data)

            self.assertEqual(user.email, "test@example.com")
            self.assertEqual(user.account_type, "lender")
            self.assertTrue(user.check_password("password123"))
            mock_save.assert_called_once()
