from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


ACCOUNT_TYPES = (
    ("lender", "lender"),
    ("borrower", "borrower"),
)


class User(AbstractUser):
    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(
        unique=True, null=False, blank=False, validators=[EmailValidator]
    )

    balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
