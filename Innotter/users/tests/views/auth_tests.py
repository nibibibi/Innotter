from unittest import mock

import jwt
import pytest

from users.models import User
from users.views import RegistrationView, LoginView
from model_bakery import baker
from rest_framework.test import APIRequestFactory
from users.serializers import UserSerializer

api_factory = APIRequestFactory()
registration_view = RegistrationView.as_view()
login_view = LoginView.as_view()
pytestmark = pytest.mark.django_db


class TestAuthLogic:
    registration_url = "/auth/register"
    login_url = "/auth/login"

    @mock.patch("Innotter.settings.SECRET_KEY", '1')
    def test_registration(self):
        user_serialization = {
            'username': "testuser",
            'email': "testuser@innowise-group.com",
            'role': "user",
            'password': "testuserpassword"
        }

        request = api_factory.post(self.registration_url, user_serialization)

        response = registration_view(request)

        assert response.status_code == 201
        user_serialization.pop('password')
        assert response.data == user_serialization

    @mock.patch("Innotter.settings.SECRET_KEY", '1')
    def test_login(self):
        user = baker.make(User)

        login_json = {
            'username': user.username,
            'password': user.password
        }

        user.set_password(user.password)
        user.save()

        request = api_factory.post(self.login_url, login_json)
        response = login_view(request)

        assert response.status_code == 200

        access_token_payload = jwt.decode(response.data.get('access_token'),
                                          'django-insecure--s*8gg=v&!+di@*(3i)ukc$6qvs%&gzv%nmy1whl51y@ls2fw3',
                                          algorithms=['HS256'])
        refresh_token_payload = jwt.decode(response.data.get('refresh_token'),
                                           'django-insecure--s*8gg=v&!+di@*(3i)ukc$6qvs%&gzv%nmy1whl51y@ls2fw3',
                                           algorithms=['HS256'])
        assert access_token_payload.get('user_id') == refresh_token_payload.get('user_id') == user.pk
        assert response.data.get('user') == UserSerializer(user).data





