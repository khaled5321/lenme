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
    path(
        "offers/<int:offer_id>/accept_offer/",
        views.AcceptOffer.as_view(),
        name="accept_offer",
    ),
    path("accepted_offers/", views.AcceptedOffers.as_view(), name="accepted_offers"),
    path(
        "accepted_offers/<int:offer_id>/fund/",
        views.FundOffer.as_view(),
        name="check_balance",
    ),
]
