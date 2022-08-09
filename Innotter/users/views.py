from asyncio import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .auth import generate_access_token, generate_refresh_token
from .serializers import UserSerializer
from .models import User
from rest_framework import exceptions

class UserView(APIView):
    def get(self, request, format=None):
        user = request.user
        serialized_user = UserSerializer(user).data
        return Response({'user': serialized_user})
    
class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None:
            raise exceptions.AuthenticationFailed("Username was not provided.")
        if password is None:
            raise exceptions.AuthenticationFailed("Password was not provided.")
        
        user = User.objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed("User does not exist.")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Wrong password.")
        
        serialized_user = UserSerializer(user).data
        
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        response = Response()
        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'user': serialized_user,
        }
        
        return response