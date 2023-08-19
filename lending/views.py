from django.core.cache import cache
from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import LenderPermission, BorrowerPermission
from .services import (
    loan_request_create,
    offer_create,
    offer_accept,
    lender_balance_check,
    offer_fund,
)
from .serializers import LoanRequestSerializer, OfferSerializer
from .models import LoanRequest, Offer

generics.ListAPIView


class LoanRequests(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanRequestSerializer

    def get_queryset(self):
        return LoanRequest.objects.filter(status="pending")

    def get(self, request):
        loan_requests_objects = cache.get("loan_requests")

        if loan_requests_objects is None:
            cache.set("loan_requests", self.get_queryset(), 60 * 15)
            loan_requests_objects = cache.get("loan_requests")

        serializer = self.serializer_class(loan_requests_objects, many=True)

        return Response(serializer.data)


class SubmitLoanRequest(APIView):
    permission_classes = [permissions.IsAuthenticated, BorrowerPermission]
    serializer_class = LoanRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        loan_request_create(request=request, data=serializer.validated_data)

        return Response(
            "loan request created successfully", status=status.HTTP_201_CREATED
        )


class SubmitOffer(APIView):
    permission_classes = [permissions.IsAuthenticated, LenderPermission]
    serializer_class = OfferSerializer

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer_create(request=request, loan_id=pk, data=serializer.validated_data)

        return Response("offer created successfully", status=status.HTTP_201_CREATED)


class Offers(APIView):
    permission_classes = [permissions.IsAuthenticated, BorrowerPermission]
    serializer_class = OfferSerializer

    def get_queryset(self, request):
        return Offer.objects.filter(loan_request__borrower=request.user)

    def get(self, request):
        offers = cache.get("offers")

        if offers is None:
            cache.set("offers", self.get_queryset(request), 60 * 15)
            offers = cache.get("offers")

        serializer = self.serializer_class(offers, many=True)

        return Response(serializer.data)


class AcceptOffer(APIView):
    permission_classes = [permissions.IsAuthenticated, BorrowerPermission]

    def get(self, request, offer_id):
        offer_accept(offer_id=offer_id)

        return Response("offer accepted successfully")


class AcceptedOffers(APIView):
    permission_classes = [permissions.IsAuthenticated, BorrowerPermission]
    serializer_class = OfferSerializer

    def get_queryset(self, request):
        return Offer.objects.filter(status="accepted")

    def get(self, request):
        offers = cache.get("accepted_offers")

        if offers is None:
            cache.set("accepted_offers", self.get_queryset(request), 60 * 15)
            offers = cache.get("accepted_offers")

        serializer = self.serializer_class(offers, many=True)

        return Response(serializer.data)


class FundOffer(APIView):
    permission_classes = [permissions.IsAuthenticated, LenderPermission]

    def get(self, request, offer_id):
        lender_balance_check(lender=request.user, offer_id=offer_id)

        offer_fund(request=request, offer_id=offer_id)

        return Response("Offer funded successfully")
