import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from .models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get("Authorization")

        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(" ")[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Access Token expired.")
        except IndexError:
            raise exceptions.AuthenticationFailed("Token prefix missing.")

        user = User.objects.get(pk=payload["user_id"])

        if user is None:
            raise exceptions.AuthenticationFailed("User does not exist.")

        if user.is_blocked:
            raise exceptions.AuthenticationFailed("User is blocked.")

        return user, None
