from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from . import services


class UserSignup(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.user_create(data=serializer.validated_data)

        return Response("account created successfully")
