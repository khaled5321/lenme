from decimal import Decimal
from django.db import models
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

LOAN_STATUS = (("pending", "pending"), ("funded", "funded"), ("completed", "completed"))
OFFER_STATUS = (
    ("pending", "pending"),
    ("accepted", "accepted"),
    ("rejected", "rejected"),
)

INTEREST_VALIDATOR = [MinValueValidator(0.03), MaxValueValidator(2.0)]


class LoanRequest(models.Model):
    borrower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="loan_requests"
    )

    loan_amount = models.DecimalField(
        default=0.01,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    loan_period = models.PositiveIntegerField(default=1)

    lenme_fee = models.DecimalField(
        default=0.01,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    status = models.CharField(default="pending", choices=LOAN_STATUS, max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_loan_amount(self):
        return self.loan_amount + self.lenme_fee

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.borrower.email

    def save(self, *args, **kwargs):
        cache.delete("loan_requests")
        super().save(*args, **kwargs)


class Offer(models.Model):
    lender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_offers"
    )
    loan_request = models.ForeignKey(
        LoanRequest, on_delete=models.CASCADE, related_name="loan_offers"
    )

    interest_rate = models.FloatField(default=0.03, validators=INTEREST_VALIDATOR)

    status = models.CharField(default="pending", choices=OFFER_STATUS, max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def interest(self):
        return (
            Decimal(self.interest_rate)
            * self.loan_request.loan_amount
            * Decimal(self.loan_request.loan_period / 12)
        )

    @property
    def total_amount_after_interest(self):
        return self.interest + self.loan_request.loan_amount

    @property
    def monthly_payment(self) -> Decimal:
        return round(
            self.total_amount_after_interest / self.loan_request.loan_period, 2
        )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return (
            f"Lender: {self.lender.email}, Borrower: {self.loan_request.borrower.email}"
        )

    def save(self, *args, **kwargs):
        cache.delete("offers")
        cache.delete("accepted_offers")
        super().save(*args, **kwargs)


class ScheduledPayment(models.Model):
    borrower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="scheduled_payments"
    )
    loan_request = models.ForeignKey(
        LoanRequest, on_delete=models.CASCADE, related_name="loan_payments"
    )
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    payment_date = models.DateTimeField()
    payment_amount = models.DecimalField(
        default=0.01,
        decimal_places=2,
        max_digits=10,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    is_complete = models.BooleanField(default=False)
    is_last_payment = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.payment_date.date()}"
