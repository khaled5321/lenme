from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import exceptions
from accounts.models import User
from .models import LoanRequest, Offer, ScheduledPayment


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
    loan_request = get_object_or_404(LoanRequest, id=loan_id)
    offer = Offer.objects.create(
        lender=request.user,
        loan_request=loan_request,
        interest_rate=data["interest_rate"],
    )
    return offer


def offer_accept(*, offer_id: int) -> None:
    offer = get_object_or_404(Offer, id=offer_id)
    offer.status = "accepted"
    offer.save()


def payment_schedule(*, offer: Offer) -> None:
    number_of_payments = offer.loan_request.loan_period
    payment_amount = offer.monthly_payment

    scheduled_payments = []

    for index in range(number_of_payments):
        payment = ScheduledPayment(
            borrower=offer.loan_request.borrower,
            loan_request=offer.loan_request,
            offer=offer,
            payment_amount=payment_amount,
        )
        payment.payment_date = timezone.now() + timedelta(days=(index + 1) * 30)
        if index == number_of_payments - 1:
            payment.is_last_payment = True

        scheduled_payments.append(payment)

    ScheduledPayment.objects.bulk_create(scheduled_payments)


def lender_balance_check(lender: User, offer_id: int) -> None:
    offer = get_object_or_404(Offer, id=offer_id)
    amount = offer.loan_request.total_loan_amount
    if lender.balance < amount:
        raise exceptions.ValidationError(
            {
                "can_fund": False,
                "detail": f"Insufficient balance: {lender.balance} < {amount}",
            }
        )


def lender_balance_deduct(lender: User, amount: Decimal) -> None:
    if lender.balance < amount:
        raise exceptions.ValidationError(
            {"detail": f"Insufficient balance: {lender.balance} < {amount}"}
        )
    lender.balance -= amount
    lender.save()


def borrower_balance_add(borrower: User, amount: Decimal) -> None:
    borrower.balance += amount
    borrower.save()


def borrower_balance_deduct(borrower: User, amount: Decimal) -> None:
    if borrower.balance < amount:
        raise exceptions.ValidationError(
            {"detail": f"Insufficient balance: {borrower.balance} < {amount}"}
        )

    borrower.balance += amount
    borrower.save()


@transaction.atomic
def offer_fund(*, request, offer_id: int):
    offer = get_object_or_404(Offer, id=offer_id)

    if offer.status != "accepted":
        raise exceptions.ValidationError({"can_fund": False})

    if offer.loan_request.status != "pending":
        raise exceptions.ValidationError({"can_fund": False})

    lender = request.user
    borrower = offer.loan_request.borrower

    lender_balance_deduct(lender=lender, amount=offer.loan_request.total_loan_amount)
    borrower_balance_add(borrower=borrower, amount=offer.loan_request.loan_amount)

    offer.loan_request.status = "funded"
    offer.loan_request.save()

    payment_schedule(offer=offer)
