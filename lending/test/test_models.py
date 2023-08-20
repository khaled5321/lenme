from django.test import TestCase
from django.core.cache import cache
from decimal import Decimal
from django.contrib.auth import get_user_model
from ..models import LoanRequest, Offer


class LoanRequestModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.borrower = self.User.objects.create(
            email="borrower@example.com", account_type="borrower"
        )
        self.loan_request = LoanRequest.objects.create(
            borrower=self.borrower,
        )
        cache.set("loan_requests", "test_value")

    def test_total_loan_amount(self):
        result = self.loan_request.total_loan_amount

        self.assertEqual(result, 0.02)

    def test_str_returns_borrower_email(self):
        result = self.loan_request.__str__()

        self.assertEqual(result, self.loan_request.borrower.email)

    def test_save_invalidate_cache(self):
        self.loan_request.save()

        self.assertEqual(cache.get("loan_requests"), None)


class OfferModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.lender = self.User.objects.create(
            email="lender@example.com", account_type="lender"
        )
        self.borrower = self.User.objects.create(
            email="borrower@example.com", account_type="borrower"
        )
        self.loan_request = LoanRequest.objects.create(
            borrower=self.borrower,
        )

        self.offer = Offer.objects.create(
            lender=self.lender,
            loan_request=self.loan_request,
        )
        cache.set("offers", "test_value")
        cache.set("accepted_offers", "test_value")

    def test_interest_property(self):
        self.offer.interest_rate = Decimal("0.05")
        self.offer.loan_request.loan_amount = Decimal("10000")
        self.offer.loan_request.loan_period = 12
        expected_interest = Decimal("500")
        self.assertEqual(self.offer.interest, expected_interest)

    def test_save_invalidate_cache(self):
        self.offer.save()

        self.assertEqual(cache.get("offers"), None)
        self.assertEqual(cache.get("accepted_offers"), None)
