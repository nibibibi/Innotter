from unittest import mock
import pytest
from users.auth import generate_access_token
from pages.tests.users_tests.conftest import user, new_user
from rest_framework.test import APIRequestFactory, force_authenticate
from pages.views.user_views import UserViewSet

pytestmark = pytest.mark.django_db
toggle_block_unblock_view = UserViewSet.as_view({'post': "toggle_block"})


class TestUserLogic:
    url = "/resource/users/"

    @mock.patch("Innotter.settings.SECRET_KEY", "1")
    def test_toggle_block_unblock(self, user: user, new_user: new_user, api_factory: APIRequestFactory):
        user_to_block = new_user
        user_to_block.save()

        token = generate_access_token(user)
        request = api_factory.post(f"{self.url}/{user_to_block.pk}/toggle_block/")
        force_authenticate(request, user=user, token=token)

        response = toggle_block_unblock_view(request, pk=user_to_block.pk)
        assert response.data.get('status') == "user blocked"
        response = toggle_block_unblock_view(request, pk=user_to_block.pk)
        assert response.data.get('status') == "user unblocked"
