import kronos
from datetime import date
from django.db import transaction
from .services import lender_balance_add, borrower_balance_deduct
from .models import ScheduledPayment


@kronos.register("0 8 * * *")
@transaction.atomic
def process_scheduled_payments():
    scheduled_payments = ScheduledPayment.objects.filter(
        payment_date__day=date.today().day, is_complete=False
    )
    for scheduled_payment in scheduled_payments:
        borrower = scheduled_payment.borrower
        lender = scheduled_payment.offer.lender

        borrower_balance_deduct(
            borrower=borrower, amount=scheduled_payment.payment_amount
        )
        lender_balance_add(lender=lender, amount=scheduled_payment.payment_amount)

        scheduled_payment.is_complete = True

        if scheduled_payment.is_last_payment:
            scheduled_payment.loan_request.status = "completed"
            scheduled_payment.loan_request.save()

        scheduled_payment.save()

        print("Processed payment")
