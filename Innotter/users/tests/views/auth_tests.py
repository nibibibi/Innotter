from unittest import mock

import pytest

from users.models import User
from users.views import RegistrationView, LoginView
from model_bakery import baker
from rest_framework.test import APIRequestFactory

api_factory = APIRequestFactory()
registration_view = RegistrationView.as_view()
login_view = LoginView.as_view()
pytestmark = pytest.mark.django_db


class TestUserLogic:
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
        assert len(response.data.get('access_token')) == len(response.data.get('refresh_token')) == 144






