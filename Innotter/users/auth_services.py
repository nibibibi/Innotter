import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .auth import generate_access_token, generate_refresh_token
from .models import User
from .serializers import UserSerializer


def log_user_in(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        raise AuthenticationFailed("Invalid login data.")

    user = User.objects.filter(username=username).first()
    if user is None:
        raise AuthenticationFailed("Incorrect username.")
    if not user.check_password(password):
        raise AuthenticationFailed("Wrong password.")

    serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    response = Response()
    response.data = {
        "refresh_token": refresh_token,
        "access_token": access_token,
        "user": serialized_user,
    }

    return response


def refresh_access_token(request):
    refresh_token = request.data.get("refresh_token")
    if refresh_token is None:
        raise AuthenticationFailed("No refresh token provided.")
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Refresh token already expired.")

    user = User.objects.get(pk=payload.get("user_id"))
    if user is None:
        raise AuthenticationFailed("User not found.")

    access_token = generate_access_token(user)
    return Response({"access_token": access_token})
