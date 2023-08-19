from rest_framework.permissions import BasePermission


class LenderPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.account_type == "lender":
            return True

        return False


class BorrowerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.account_type == "borrower":
            return True

        return False
