from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .auth_services import log_user_in, refresh_access_token
from .models import User
from .serializers import RegisterSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response(log_user_in(request), status=200)


class RegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return refresh_access_token(request)
