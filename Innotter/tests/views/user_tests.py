from unittest import mock

import pytest
from users.views import RegistrationView
from rest_framework.test import APIRequestFactory

api_factory = APIRequestFactory()
view = RegistrationView.as_view()


class TestUserLogic:
    endpoint = "/resource/users/"

    @pytest.mark.django_db
    @mock.patch("users.serializers.RegisterSerializer.save")
    def test_register(self, mock_save):
        mock_save.return_value = True

        user_json = {
            "user": {
                "email": "someuser@example.com",
                "username": "someuser",
                "password": "somepassword"
            }
        }

        request = api_factory.post(
            self.endpoint,
            user_json,
            format="json",
        )

        response = view(request)

        assert response.status_code == 201