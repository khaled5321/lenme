from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user_obj = self.User.objects.create(
            email="test@example.com",
        )

    def test_str_returns_email(self):
        result = self.user_obj.__str__()

        self.assertEqual(result, "test@example.com")
