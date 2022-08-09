from asyncio import exceptions

import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import generate_access_token, generate_refresh_token
from .models import User
from .serializers import UserSerializer


class UserView(APIView):
    def get(self, request, format=None):
        user = request.user
        serialized_user = UserSerializer(user).data
        return Response({"user": serialized_user})


class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None:
            raise exceptions.AuthenticationFailed("Username was not provided.")
        if password is None:
            raise exceptions.AuthenticationFailed("Password was not provided.")

        user = User.objects.get(username=username)
        if user is None:
            raise exceptions.AuthenticationFailed("User does not exist.")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Wrong password.")

        serialized_user = UserSerializer(user).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        response = Response()
        response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
        response.data = {
            "access_token": access_token,
            "user": serialized_user,
        }

        return response


class RefreshTokenView(APIView):
    def post(self, request, format=None):
        refresh_token = request.COOKIES.get("refreshtoken")
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                "Authentication credentials were not provided."
            )
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Refresh token is expired.")

        user = User.objects.get(pk=payload.get("user_id"))
        if user is None:
            raise exceptions.AuthenticationFailed("User does not exist.")
        if user.is_blocked:
            raise exceptions.AuthenticationFailed("User is blocked.")

        access_token = generate_access_token(user)
        return Response({"access_token": access_token})
