from django.urls import path
from . import views

urlpatterns = [
    path("loan_requests/", views.LoanRequests.as_view(), name="loan_requests"),
    path(
        "loan_requests/submit_loan_request/",
        views.SubmitLoanRequest.as_view(),
        name="offers",
    ),
    path(
        "loan_requests/<int:pk>/make_offer/",
        views.SubmitOffer.as_view(),
        name="make_offer",
    ),
    path("offers/", views.Offers.as_view(), name="offers"),
    path("offers/<int:pk>/accept_offer/", views.Offers.as_view(), name="accept_offer"),
]
