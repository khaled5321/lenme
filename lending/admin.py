from django.contrib import admin
from .models import LoanRequest, Offer, ScheduledPayment

admin.site.register(LoanRequest)
admin.site.register(Offer)
admin.site.register(ScheduledPayment)
