from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import LoanRequest, Offer


class LoanRequestSerializer(serializers.ModelSerializer):
    borrower = UserSerializer(read_only=True)

    class Meta:
        model = LoanRequest
        fields = "__all__"
        read_only_fields = ["lenme_fee", "status"]


class OfferSerializer(serializers.ModelSerializer):
    lender = UserSerializer(read_only=True)
    loan_request = LoanRequestSerializer(read_only=True)
    monthly_payment = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "lender",
            "loan_request",
            "interest_rate",
            "monthly_payment",
            "created_at",
        ]

    def get_monthly_payment(self, obj):
        return obj.monthly_payment
