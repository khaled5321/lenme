from django.shortcuts import get_object_or_404
from .models import LoanRequest, Offer


def loan_request_create(*, request, data: dict) -> LoanRequest:
    loan_request = LoanRequest.objects.create(
        borrower=request.user,
        loan_amount=data["loan_amount"],
        loan_period=data["loan_period"],
        lenme_fee=3.00,
        status="pending",
    )
    return loan_request


def offer_create(*, request, loan_id: int, data: dict) -> Offer:
    offer = Offer.objects.create(
        lender=request.user,
        loan_request=LoanRequest.objects.get(id=loan_id),
        interest_rate=data["interest_rate"],
    )
    return offer


def lender_balance_deduct(*args, **kwargs):
    pass


def loan_fund(*args, **kwargs):
    pass


def payment_schedule(*args, **kwargs):
    pass


def offer_accept(*, request, offer_id: int) -> Offer:
    offer = get_object_or_404(Offer, id=offer_id)
