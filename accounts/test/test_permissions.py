from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from lending.models import LoanRequest
from ..permissions import LenderPermission, BorrowerPermission


class PrepareTest(TestCase):
    def setUp(self):
        self.User = get_user_model()

        self.lender_user = self.User.objects.create(
            username="author", email="lender@gmail.com", account_type="lender"
        )

        self.borrower_user = self.User.objects.create(
            email="borrower@gmail.com", account_type="borrower"
        )

        self.loan_request = LoanRequest.objects.create(
            borrower=self.borrower_user,
        )

        self.factory = RequestFactory()


class LenderPermissionTest(PrepareTest):
    def test_lender_can_make_offer(self):
        request = self.factory.post("/api/v1/loan_requests/1/make_offer/")
        request.user = self.lender_user

        permission_check = LenderPermission()

        permission = permission_check.has_permission(request, None)

        self.assertTrue(permission)

    def test_lender_user_cant_submit_loan_request(self):
        request = self.factory.post("/api/v1/loan_requests/submit_loan_request/")
        request.user = self.lender_user

        permission_check = BorrowerPermission()

        permission = permission_check.has_permission(request, None)

        self.assertFalse(permission)


class BorrowerPermissionTest(PrepareTest):
    def test_borrower_cant_make_offer(self):
        request = self.factory.post("/api/v1/loan_requests/1/make_offer/")
        request.user = self.borrower_user

        permission_check = LenderPermission()

        permission = permission_check.has_permission(request, None)

        self.assertFalse(permission)

    def test_lender_user_can_submit_loan_request(self):
        request = self.factory.post("/api/v1/loan_requests/submit_loan_request/")
        request.user = self.borrower_user

        permission_check = BorrowerPermission()

        permission = permission_check.has_permission(request, None)

        self.assertTrue(permission)
